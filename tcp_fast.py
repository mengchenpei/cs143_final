import collections
import events

class TcpFast():
    '''
        Main class for TcpFast
        
        Attributes:
            windowSize: the window size of current Flow
            threshold: Slow Start Threshold
            avgRTT: average value of Round Trip Time
            alpha: parameter for TCP Fast
            gamma: renew rate for avgRTT. i.e.
                   i.e. self.avgRTT = (1 - self.gamma) * self.avgRTT + self.gamma * RTT
            baseRTT: base RTT
            onTheFly: all packets in transmission (Haven't been ACKed)
            acknowledgedPacketID: the next ACK packet ID to be expected
            validTimeOutEvent: Used for handling time_out event
            stateMachine: state machine for TCP         
    '''
    def __init__(self):
        self.windowSize = 4
        self.threshold = 16
        self.avgRTT = 0
        self.alpha = 16
        self.gamma = 0.5
        self.baseRTT = float('inf')
        self.onTheFly = collections.deque()
        self.acknowledgedPacketID = -1
        self.validTimeOutEvent = None
        self.stateMachine = StateMachine(self)


    def setFlow(self, flow):
        '''
            Associate current TCP with the corresponding Flow
            One flow has only one specific TCP
            One TCP associated with only one Flow
            
            Args:
                flow: flow to be connected
        '''
        self.flow = flow
        self.engine = self.flow.engine

        
    def setWindowSize(self, windowSize):
        '''
            Set and log current window size
            
            Args:
                windowSize: window size to be set
        '''
        self.windowSize = windowSize
        self.engine.recorder.record_window_size(self.flow, self.engine.getCurrentTime(), 
                                                self.windowSize)

        
    def sendNewPackets(self):
        '''
            Start sending out new packets
        ''' 
        count = 2
        while len(self.onTheFly) < self.windowSize and count >0:
            count -=1
            if len(self.onTheFly) == 0: 
                self.sendPacket(self.acknowledgedPacketID+1)
                self.onTheFly.append(self.acknowledgedPacketID+1)
            else:
                self.sendPacket(self.onTheFly[-1]+1)
                self.onTheFly.append(self.onTheFly[-1]+1)

            
    def sendPacket(self, pck_id):
        '''
            Send out a packet with specific pck_id
            
            Args:
                pck_id: id of the specific packet to be sent
        ''' 
        if pck_id < self.flow.amount:
            packet = self.flow.generatePacket(pck_id)
            self.flow.sourceSend(packet)
            self.setTimeOutEvent(max(1, self.avgRTT))


    def receiveACK(self, ackPacket):
        '''
            When a new ACK packet is received, renew acknowledgedPacketID and onTheFly
            
            Args:
                ackPacket: ACK packet received
        '''  
        pck_id = ackPacket.pck_id
        self.acknowledgedPacketID  = max(self.acknowledgedPacketID, pck_id-1)
        while len(self.onTheFly) > 0 and self.onTheFly[0] <= self.acknowledgedPacketID:
            self.onTheFly.popleft()
        
        self.engine.recorder.record_pkts_received(self.flow, self.engine.getCurrentTime(), self.acknowledgedPacketID)        

            
    def setTimeOutEvent(self, delay):
        '''
            Set time_out event and add it to the Event Queue
            
            Args:
                delay: specify delay for time_out event
        '''
        event = events.Event.CreateEventPacketTimeOut(self.engine.getCurrentTime()+ delay, self.flow)
        self.validTimeOutEvent = event
        self.engine.push_event(event)

        
    def react_to_flow_start(self, event):
        '''
            [Called by Flow]
            React to the start of Flow, start sending out the first packet
            
            Args:
                event: event to be reacted to, which should be EVENT_FLOW_START here
        '''  
        self.sendPacket(0)

        
    def react_to_time_out(self, event):
        '''
            Call self.stateMachine.timeout() to handle time_out event
            
            Args:
                event: event to be reacted to, which should be EVENT_PACKET_TIMEOUT here
        '''
        if event != self.validTimeOutEvent:
            return
        self.stateMachine.timeout()
            

    def react_to_ack(self, packet):
        '''
            [Called by Flow]
            When received ACK, TCP will
                1) calculate RTT, including baseRTT and avgRTT
                2) Call self.reveivedACK to handle ACK packet received
                3) Call self.stateMachine.ACK for TCP Phase Control
                4) Call self.sendNewPackets to start sending out new packets
            
            Args:
                packet: the ACK packet received
        '''           
        RTT = self.engine.getCurrentTime() - packet.originalPacketTimestamp
        self.baseRTT = min(self.baseRTT,RTT)
        self.avgRTT = (1-self.gamma) * self.avgRTT + self.gamma * RTT
        self.receiveACK(packet)
        self.stateMachine.ACK(packet, RTT)
        self.sendNewPackets()



class StateMachine(object):
    '''
        StaeMachine is used for TCP Phase Control
        
        Attributes:
            state: current state of the State Machine
            algorithm: the corresponding algorithm, which is the corresponding TCP_Fast
            lastAckID: ID of the latest ACK that has already been ACKed
            dupTime: count how many duplicate ACKs have been received for the same packet,
                     which will be reset after a new packet has been received
    '''
    SLOW_START = 'slow_start'
    CONGESTION_CONTROL = 'congestion_control'
    FAST_RETRANSMIT = 'fast_retransmit'
    DONE = 'done'
    def __init__(self, algorithm):
        self.state = StateMachine.SLOW_START
        self.algorithm = algorithm
        self.lastAckID = -1
        self.dupTime = 0


    def ACK(self, ackPacket, RTT):
        '''
            Main function to handle the receive of a ACK packet
            
            SLOW_START:
                slow start phase,
                    if dupTime < 3,
                        if W < ssThre, W = W + 1
                        if W >= ssThre, W = W + 1 / W, enter CONGESTION_CONTROL
                    else,
                        handle DUP_ACK, enter Fast Retransmission
                        
            CONGESTION_CONTROL:
                congestion avoidance phase,
                    if dupTime < 3,
                        windowSize = min(2*windowSize, (1-self.algorithm.gamma)*windowSize + 
                        self.algorithm.gamma*(self.algorithm.baseRTT/RTT*windowSize + self.algorithm.alpha))
                    else,
                        handle DUP_ACK, enter Fast Retransmission
            
            FAST_RETRANSMIT:
                stands for FR/FR
                    if dupTime > 3,
                        W = W + 1
                    else,
                        1) handle
                        2) return back to CONGESTION_CONTROL
            
            DONE:
                all data transmission has finished.
                Set window size to 0
                
            Args:
                ackPacket: current ACK packet to be handled
                RTT: the RTT of the ACK packet
        '''
        if self.lastAckID == ackPacket.pck_id:
            self.dupTime += 1
        else:
            self.dupTime = 0
            self.lastAckID = ackPacket.pck_id
            
        if ackPacket == self.algorithm.flow.amount:
            self.state = StateMachine.DONE
            self.algorithm.setWindowSize(0)
            
        if self.state == StateMachine.DONE:
            return
        
        if self.state == StateMachine.SLOW_START:
            if self.dupTime <3:
                if self.algorithm.windowSize < self.algorithm.threshold:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1)
                else:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1.0/self.algorithm.windowSize)
                    self.state = StateMachine.CONGESTION_CONTROL
                    event = events.Event.CreateEventFastUpdate(self.algorithm.engine.getCurrentTime()+ self.algorithm.avgRTT, self)
                    self.algorithm.engine.push_event(event)
                return
            
            if self.dupTime >= 3:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(self.algorithm.windowSize/2.0+3)                
                self.algorithm.sendPacket(ackPacket.pck_id)                
                return
                
        if self.state == StateMachine.CONGESTION_CONTROL:
            if self.dupTime <3:
                
                return
            
            if self.dupTime >= 3:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(self.algorithm.windowSize/2.0+3)                
                self.algorithm.sendPacket(ackPacket.pck_id)
                return

        if self.state == StateMachine.FAST_RETRANSMIT:
                        
            if self.dupTime > 3:
                self.algorithm.setWindowSize(self.algorithm.windowSize+1)
            else:
                self.algorithm.setWindowSize(self.algorithm.threshold)
                self.state = StateMachine.CONGESTION_CONTROL
                event = events.Event.CreateEventFastUpdate(self.algorithm.engine.getCurrentTime()+self.algorithm.avgRTT, self)
                self.algorithm.engine.push_event(event)
                
            return
            
        self.engine.recorder.record_ssthre(self.flow, self.engine.getCurrentTime(), 
                                           self.threshold)    

            
    def timeout(self):
        '''
            React to packet timeout
                1) set ssThre = W / 2
                2) W = 1
                3) enter SLOW_START
                4) empty all the packets on transmission
                5) start sending new packets
        '''
        self.algorithm.threshold = self.algorithm.windowSize/2
        self.algorithm.setWindowSize(1)
        self.state = StateMachine.SLOW_START
        self.algorithm.onTheFly = collections.deque()
        self.algorithm.sendNewPackets()


    def react_fast_update(self, _):
        
        if self.state != self.CONGESTION_CONTROL:
            return
        event = events.Event.CreateEventFastUpdate(self.algorithm.engine.getCurrentTime()+self.algorithm.avgRTT, self)
        self.algorithm.engine.push_event(event)
        windowSize = self.algorithm.windowSize       
        windowSize = min(2*windowSize, (1-self.algorithm.gamma)*windowSize + 
                         self.algorithm.gamma*(self.algorithm.baseRTT/self.algorithm.avgRTT*windowSize + self.algorithm.alpha))
        self.algorithm.setWindowSize(windowSize)
        

