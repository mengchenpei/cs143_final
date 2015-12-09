'''
    TCP Reno, which enables Fast Recovery & Fast Retransmission
'''
import collections
import events

class TcpReno():
    '''
        Main class for TcpReno
        
        Attributes:
            # initialized in __init__(self)
            windowSize: the window size of current Flow
            threshold: Slow Start Threshold
            firstAck: flag to indicate if current ACK is the first ACK,
                      used to set the initial value of avgRTT and divRTT
            avgRTT: average value of Round Trip Time
            divRTT: divergence of Round Trip Time
            alpha: renew rate for divRTT. 
                   i.e. self.divRTT = (1 - self.alpha) * self.divRTT + self.alpha * abs(RTT - self.avgRTT)
            gamma: renew rate for divRTT. i.e.
                   i.e. self.avgRTT = (1 - self.gamma) * self.avgRTT + self.gamma * RTT
            onTheFly: all packets in transmission (Haven't been ACKed)
            acknowledgedPacketID: the next ACK packet ID to be expected
            validTimeOutEvent: Used for handling time_out event
            
            # initialized in setFlow(self, flow)
            flow: associate current TCP with the corresponding Flow
            engine: set current engine, mainly for data log
            stateMachine: state machine for TCP         
    '''
    def __init__(self):
        '''
            Initialization of a TCP_Reno
        '''
        self.windowSize = 4
        self.threshold = 500
        
        self.firstAck = True
        self.avgRTT = 1
        self.divRTT = 0
        self.alpha = 0.25
        self.gamma = 0.125
        
        self.onTheFly = collections.deque()
        self.acknowledgedPacketID = -1
        self.validTimeOutEvent = None
        
        
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
        self.stateMachine = StateMachine(self, flow)
    

    def setWindowSize(self, windowSize):
        '''
            Set and log current window size
            
            Args:
                windowSize: window size to be set
        '''
        self.windowSize = windowSize
        self.engine.recorder.record_window_size(self.flow, self.engine.getCurrentTime(), 
                                                self.windowSize)
    
    
    def react_to_flow_start(self, event):
        '''
            [Called by Flow]
            React to the start of Flow, start sending out the first packet
            
            Args:
                event: event to be reacted to, which should be EVENT_FLOW_START here
        '''   
        self.sendPacket(0)
    

    def sendNewPackets(self):
        '''
            Start sending out new packets
        ''' 
        count = 2
        while len(self.onTheFly) < self.windowSize and count > 0:
            count -= 1
            if len(self.onTheFly) == 0: 
                self.sendPacket(self.acknowledgedPacketID + 1)
                self.onTheFly.append(self.acknowledgedPacketID + 1)
            else:
                self.sendPacket(self.onTheFly[-1] + 1)
                self.onTheFly.append(self.onTheFly[-1] + 1)
   
        
    def sendPacket(self, pck_id):
        '''
            Send out a packet with specific pck_id
            
            Args:
                pck_id: id of the specific packet to be sent
        '''  
        if pck_id < self.flow.amount:
            packet = self.flow.generatePacket(pck_id)
            self.flow.sourceSend(packet)
            
            # According to the textbook, set avg + 4 * div to be the time_out delay
            tempTimeOut = 1 * self.avgRTT + 4 * self.divRTT
            
            # Set a time_out event for every packet
            self.setTimeOutEvent(tempTimeOut)

            self.engine.recorder.record_timeout(self.flow, self.engine.getCurrentTime(), 
                                                tempTimeOut)
    

    def react_to_ack(self, packet):
        '''
            [Called by Flow]
            When received ACK, TCP will
                1) calculate RTT, including avgRTT and divRTT
                2) Call self.reveivedACK to handle ACK packet received
                3) Call self.stateMachine.ACK for TCP Phase Control
                4) Call self.sendNewPackets to start sending out new packets
            
            Args:
                packet: the ACK packet received
        '''
        # Calculate RTT based on current time and packet time_stamp
        RTT = self.engine.getCurrentTime() - packet.originalPacketTimestamp

        if self.firstAck:
            # On first ACK packet received, set the initial value for avgRTT and divRTT
            self.avgRTT = RTT
            self.divRTT = RTT
            self.firstAck = False
        else:
            # if it's not the first packet, just renew avgRTT and divRTT
            self.avgRTT = (1 - self.gamma) * self.avgRTT + self.gamma * RTT
            self.divRTT = (1 - self.alpha) * self.divRTT + self.alpha * abs(RTT - self.avgRTT)

        self.engine.recorder.record_ssthre(self.flow, self.engine.getCurrentTime(), 
                                           self.threshold)
        self.engine.recorder.record_rtt(self.flow, self.engine.getCurrentTime(), 
                                        RTT)
        self.receiveACK(packet)
        self.stateMachine.ACK(packet, RTT)
        self.sendNewPackets()
                  
                        
    def receiveACK(self, ackPacket):
        '''
            When a new ACK packet is received, renew acknowledgedPacketID and onTheFly
            
            Args:
                ackPacket: ACK packet received
        '''  
        pck_id = ackPacket.pck_id
        self.acknowledgedPacketID  = max(self.acknowledgedPacketID, pck_id-1)
        
        self.engine.recorder.record_pkts_received(self.flow, self.engine.getCurrentTime(), self.acknowledgedPacketID)        
        
        # Pop out all packets that should already been received
        while len(self.onTheFly) > 0 and self.onTheFly[0] <= self.acknowledgedPacketID:
            self.onTheFly.popleft()

       
    def setTimeOutEvent(self, delay):
        '''
            Set time_out event and add it to the Event Queue
            
            Args:
                delay: specify delay for time_out event
        '''
        event = events.Event.CreateEventPacketTimeOut(self.engine.getCurrentTime()+ delay, self.flow)
        self.validTimeOutEvent = event
        self.engine.push_event(event)


    def react_to_time_out(self, event):
        '''
            Call self.stateMachine.timeout() to handle time_out event
            
            Args:
                event: event to be reacted to, which should be EVENT_PACKET_TIMEOUT here
        '''
        if event != self.validTimeOutEvent:
            return
        self.stateMachine.timeout()



class StateMachine(object):
    '''
        StaeMachine is used for TCP Phase Control
        
        Attributes:
            # initialized in self.__init__(self, algorithm, flow)
            state: current state of the State Machine
            algorithm: the corresponding algorithm, which is the corresponding TCP_Reno
            lastAckID: ID of the latest ACK that has already been ACKed
            dupTime: count how many duplicate ACKs have been received for the same packet,
                     which will be reset after a new packet has been received
            flow: the associated flow
            lastRetrans: the time stamp for the last FR/FR event
            lastRetransPckID: the packet retransmitted for the last FR/FR event
            minIntervalForRetrans: the minimum interval for handling two Time_Out / Dup_ACK events
    '''
    SLOW_START = 'slow_start'
    CONGESTION_CONTROL = 'congestion_control'
    FAST_RETRANSMIT = 'fast_retransmit'
    DONE = 'done'
    def __init__(self, algorithm, flow):
        '''
            Initialization
            
            Args:
                algorithm: the TCP associated with current state machine
                flow: the flow associated with current state machine
        '''
        self.state = StateMachine.SLOW_START
        self.algorithm = algorithm
        self.lastAckID = -1
        self.dupTime = 0
        self.flow = flow
        self.lastRetrans = -1
        self.lastRetransPckID = -1
        # set the default value of minIntervalForRetrans to be 0.5s
        self.minIntervalForRetrans = 0.5
        

    def ACK(self, ackPacket, RTT):
        '''
            Main function to handle the receive of a ACK packet
            
            SLOW_START:
                slow start phase,
                    if dupTime < 3,
                        if W < ssThre, W = W + 1
                        if W >= ssThre, W = W + 1 / W, enter CONGESTION_CONTROL
                    else,
                        handle DUP_ACK, enter FR/FR (only handle once every minIntervalForRetrans)
                        
            CONGESTION_CONTROL:
                congestion avoidance phase,
                    if dupTime < 3,
                        W = W + 1 / W
                    else,
                        handle DUP_ACK, enter FR/FR (only handle once every minIntervalForRetrans)
            
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
        # Calculate for dupTime
        if self.lastAckID == ackPacket.pck_id:
            print ackPacket.pck_id
            self.dupTime += 1
        else:
            self.dupTime = 0
            self.lastAckID = ackPacket.pck_id

        self.flow.engine.recorder.record_dup_times(self.flow, self.flow.engine.getCurrentTime(), self.dupTime)
        
        if ackPacket == self.algorithm.flow.amount:
            self.state = StateMachine.DONE
            self.algorithm.setWindowSize(0)
            
        if self.state == StateMachine.DONE:
            return
        
        if self.state == StateMachine.SLOW_START:
            self.flow.engine.recorder.record_state(self.flow, self.flow.engine.getCurrentTime(), 
                                       1)
            if self.dupTime < 3:
                if self.algorithm.windowSize < self.algorithm.threshold:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1)
                else:
                    self.algorithm.setWindowSize(self.algorithm.windowSize+1.0/self.algorithm.windowSize)
                    self.state = StateMachine.CONGESTION_CONTROL
                return
            
            if self.dupTime >= 3 and self.flow.engine.getCurrentTime() > self.lastRetrans + self.minIntervalForRetrans:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(max(self.algorithm.windowSize/2.0, 2))                
                self.algorithm.sendPacket(ackPacket.pck_id)
                self.lastRetransPckID = ackPacket.pck_id
                self.dupTime = 0
                return
                
        if self.state == StateMachine.CONGESTION_CONTROL:
            self.flow.engine.recorder.record_state(self.flow, self.flow.engine.getCurrentTime(), 
                                       2)
            if self.dupTime <3:
                self.algorithm.setWindowSize(self.algorithm.windowSize+1.0/self.algorithm.windowSize)
                return
            
            if self.dupTime >= 3 and self.flow.engine.getCurrentTime() > self.lastRetrans + self.minIntervalForRetrans:
                self.state = StateMachine.FAST_RETRANSMIT
                self.algorithm.threshold = self.algorithm.windowSize/2.0
                self.algorithm.setWindowSize(max(self.algorithm.windowSize/2.0, 2))                
                self.algorithm.sendPacket(ackPacket.pck_id)
                self.lastRetransPckID = ackPacket.pck_id
                self.dupTime = 0
                return
            
        if self.state == StateMachine.FAST_RETRANSMIT:
            self.lastRetrans = self.flow.engine.getCurrentTime()
            
            self.flow.engine.recorder.record_state(self.flow, self.flow.engine.getCurrentTime(), 
                                       3)  
                                  
            if self.dupTime > 3:
                self.algorithm.setWindowSize(self.algorithm.windowSize + 1)
            else:
                self.algorithm.setWindowSize(self.algorithm.threshold)                
                self.state = StateMachine.CONGESTION_CONTROL
            return


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




