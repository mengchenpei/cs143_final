from events import *
from constants import *

import collections
import copy
import heapq

class Packet(object):
    '''
        Definition for Packet, there are two kinds of packets:
            1. DataPacket
            2. RouterPacket
        
        Attributes:
            source: the source host of current packet
            destination: the destination host of current packet
            timestamp: the time when current packet is made
            packetsize: the size of current packet
    '''
    def __init__(self, source, destination, timestamp, packetsize):
        self.source = source
        self.destination = destination
        self.timestamp = timestamp
        self.packetsize = packetsize



class DataPacket(Packet):
    '''
        Data Packet, which is generated from Packet, used for data transmission (data & ACK)
        
        Attributes:
            source: the source host of current packet
            destination: the destination host of current packet
            timestamp: the time when current packet is made
            packetsize: the size of current packet
            acknowledgement: flag for whether current packet has been received
            pck_id: unique ID for a Data Packet in a data flow 
            originalPacketTimestamp: the time when the original packet is made  
    '''
    def __init__(self, source, destination, flow, timestamp, packetsize, acknowledgement, pck_id):
        super(DataPacket, self).__init__(source = source, destination = destination,
                                         timestamp = timestamp,packetsize = packetsize)
        self.acknowledgement = acknowledgement 
        self.flow = flow
        self.pck_id = pck_id


    def setOriginalPacketTimestamp(self, timestamp):
        '''
            Set the packet with a specific timestamp
            
            Args:
                timestamp: time_stamp to be added
        '''
        self.originalPacketTimestamp = timestamp



class RouterPacket(Packet):
    '''
        Router Packet, which is generated from Packet, used for data transmission
        It does not contain flow info.generate in Router and use link to transmit
        
        Attributes:
            source: the source host of current packet
            destination: the destination host of current packet
            timestamp: the time when current packet is made
            packetsize: the size of current packet
            
            routerTable: router table to be transmitted
            type: type of current router packet.
                  1) 'request'
                  2) 'ack_request'
                  3) 'update'
    '''
    def __init__(self, source, timestamp, packetsize, routerTable, type = None):
        super(RouterPacket, self).__init__(source = source, destination = 0,
                                           timestamp = timestamp, packetsize = packetsize)
        self.routerTable = routerTable
        self.type = type



class Element(object):
    '''
        Super class for Host, Link, Buffer, Router and Flow
        
        Attributes:
            engine: engine associated, used for simulation
            name: a specific name
    '''
    def __init__(self, engine, name = None):
        self.engine = engine
        self.name = name



class Host(Element):
    '''
        Host
        
        Attributes:
            engine: engine associated, used for simulation
            name: a specific name
            address: the IP address
            link: the link associated with current host.
                  one host can have one and only one link
            flows: the flows associated with current host.
    '''
    def __init__(self, engine, name, address):    
        super(Host, self).__init__(engine, name)
        self.link = None
        self.flows = []
        self.address = address
        
    def addFlow(self, flow):
        '''
            Associate flow with current host
            
            Args:
                flow: the flow to be associated
        '''
        self.flows.append(flow)
        
    def send(self, packet):
        '''
            Use associated link to send out one packet
            
            Args:
                packet: the packet to be sent
        '''
        self.link.send(packet, self)
        
    def receive(self, packet):
        '''
            Handle the receive of a packet
            
            For Data Packet,
                Call flow.sourceReceive or flow.destinationReceive to handle it
                
            For Router Packet,
                handle 'request' packet, calculate and send out
            
            Args:
                packet: packet received
        '''
        if isinstance(packet, DataPacket):
            if packet.flow in self.flows:
                for flow in self.flows:
                    if self == flow.source:
                        flow.sourceReceive(packet)
                    if self == flow.destination:
                        flow.destinationReceive(packet)
        if isinstance(packet, RouterPacket):
            if packet.type == 'request':
                comeCost = self.engine.getCurrentTime() - packet.timestamp
                ackRouterPacket = RouterPacket(self, packet.timestamp, PACKET_SIZE, comeCost, 'ack_request')
                self.send(ackRouterPacket)
    
    def react_to_packet_receipt(self, event):
        '''
            Used to react to an EVENT_PACKET_RECEIPT event
            Call self.receive to handle it
            
            Args:
                event: event to be reacted to, which should be EVENT_PACKET_RECEIPT here
        '''
        self.receive(event.packet)


    
class Link(Element):
    '''
        Link is used for basic data transmission.
        Use two buffers and a Decide function to realize half-duplex transmission
        
        Attributes:
            engine: engine associated, used for simulation
            name: a specific name
            node1: the source node
            node2: the destination node
            propogationDelay: current link delay
            buffer1: buffer associated with data transmission from source to destination
            buffer2: buffer associated with data transmission from destination to source
            busy: a Boolean value, current status of link        
    '''
    def __init__(self, engine, name, node1, node2, delay, rate, buffer_size):
        super(Link, self).__init__(engine, name)
        self.node1 = node1
        self.node2 = node2
        self.propogationDelay = delay
        self.rate = rate
        self.buffer1 = Buffer(self.engine, self.name+'a', buffer_size, self)
        self.buffer2 = Buffer(self.engine, self.name+'b', buffer_size, self)
        self.busy = False
        self.attachToNode(node1)
        self.attachToNode(node2)
    
    def attachToNode(self, node):
        '''
            Attach current link to a node
            The node can be a Host or Router
            
            Args:
                node: the node (Host or Router) to be associated
        '''
        if isinstance(node, Host):
            if node.link != None:
                # print "ERROR: Host should not have link now"
                return            
            node.link = self
        if isinstance(node, Router):
            if node == self.node1:
                node.links.append((self, 1))
            if node == self.node2:
                node.links.append((self, 2))


    def send(self, packet, sender):
        '''
            Function for packet sending
                1) push buffer
                2) Call self.decide() for data transmission
                
            Args:
                packet: the packet to be sent
                sender: specify the source of packet, use corresponding buffer for sending
        '''
        if sender == self.node1:
            self.buffer1.push(packet)
        if sender == self.node2:
            self.buffer2.push(packet)
           
        if not self.busy:
            self.decide()
            
    def decide(self):
        '''
            Main function for half-duplex data transmission
                1) Calculate the amount of buffer packets and decide for fair transmission
                   Buffer has larger amount of packets has priority to send
                2) Calculate link delay
                3) Reschedule 2 events: let receive to receive and let link to send next packet
        '''
        lg1 = len(self.buffer1.buffer); lg2 = len(self.buffer2.buffer)
        if lg1 == 0 and lg2 == 0:
            return
        
        self.busy = True
        
        self.engine.recorder.record_link_rate(self, self.engine.getCurrentTime(), self.rate*8/1024/1024)
        popper = None
        receiver = None
        
        if lg1 == 0:
            popper = self.buffer2
            receiver = self.node1
        elif lg2 == 0:
            popper = self.buffer1
            receiver = self.node2
        else:
            if lg1 > lg2:
                popper = self.buffer1
                receiver = self.node2
            else:
                popper = self.buffer2
                receiver = self.node1

        packet = popper.pop()
        
        transmissionDeley = 1.0*packet.packetsize / self.rate
        delay = self.propogationDelay + transmissionDeley
        event1 = Event.CreateEventPacketReceipt(self.engine.getCurrentTime() + delay, receiver, packet)
        self.engine.push_event(event1)
        
        event2 = Event(self.engine.getCurrentTime() + transmissionDeley, self, EVENT_LINK_AVAILABLE)
        self.engine.push_event(event2)


    def react_to_link_available(self, event):
        '''
            Function used for data transmission
            
            Args:
                event: event to be reacted to, which should be EVENT_LINK_AVAILABLE here
        '''
        self.busy = False
        self.engine.recorder.record_link_rate(self, self.engine.getCurrentTime(), 0)
        self.decide()



class Buffer(Element):
    '''
        Each buffer accociates with one link
        
        Attributes:
            engine: engine associated, used for simulation
            name: a specific name
            buffer: a queue to store pending packets
            bytes: total amount of data in the buffer
            link: link associated with the buffer           
    '''
    def __init__(self, engine, name, buffer_size, link):
        super(Buffer, self).__init__(engine, name)
        self.buffer = collections.deque()
        self.bytes = 0
        self.buffer_size = buffer_size
        self.link = link


    def push(self, packet):
        '''
            Push new packets into the buffer
            
            If buffer can fit the new packet, add it to the data queue
            Else, handle packet lost
            
            Args:
                packet: packet waiting to be transmitted
        '''
        if self.bytes + packet.packetsize <= self.buffer_size:
            self.buffer.append((self.engine.getCurrentTime(), packet))
            self.bytes += packet.packetsize
            
            self.engine.recorder.record_packet_loss(self, self.engine.getCurrentTime(), 0)
            self.engine.recorder.record_buffer_occupancy(self, self.engine.getCurrentTime(), 1.0 * self.bytes/PACKET_SIZE)
        else:
            print "packet loss"
            if isinstance(packet, DataPacket):
                self.engine.recorder.record_packet_loss(self, self.engine.getCurrentTime(), 1)
                self.engine.recorder.record_buffer_occupancy(self, self.engine.getCurrentTime(), 1.0 * self.bytes/PACKET_SIZE)
                print 'Packet Lost: [{}],'.format(packet.pck_id)


    def pop(self):
        '''
            Pop out a packet from the queue and change the bytes of current buffer accordingly
            
            Return:
                packet: if there is a packet in the queue, return the packet
        '''
        if self.bytes == 0 :
            print "Buffer underflow"
        else:
            time, packet = self.buffer.popleft()
            self.bytes -= packet.packetsize
            self.engine.recorder.record_buffer_occupancy(self, self.engine.getCurrentTime(), 1.0 * self.bytes/PACKET_SIZE)
            return packet



class Router(Element):
    '''
        Router
        
        Attributes:
            address: the IP address
            updateTime: a specific time interval for routing table update
            links: all links associated with the router
            defaultLink: the default link to be used
            rt: routing table
                key: host ip addre, value: 1:cost; 2:next hop
    '''
    def __init__(self, engine, name, address, updateTime = ROUTER_PACKET_GENERATION_INTERVAL):
        super(Router,self).__init__(engine, name)
        self.address = address
        self.updateTime = updateTime
        self.links = []
        self.defaultLink = None
        self.rt = {}
        self.rt[address] = (0, address)
    


               
    def broadcastRouterPacket(self):
        '''
            be called when it is time to update routing table
            Broadcast Router Packet (update)
            Call link.send for data transmission
        '''
        routerPacket =  RouterPacket(self, self.engine.getCurrentTime(), PACKET_SIZE, copy.copy(self.rt), 'update')
        for link in self.links:
            if link[1] == 1:
                link[0].send(routerPacket, self)
            if link[1] == 2:
                link[0].send(routerPacket, self)


    def broadcastRequestPacket(self):
        '''
            be called when a router is initialized. 
            Broadcast Router Packet (request)
            Call link.send for data transmission
        '''
        routerPacket =  RouterPacket(self, self.engine.getCurrentTime(), PACKET_SIZE, None, 'request')
        for link in self.links:
            if link[1] == 1:
                link[0].send(routerPacket, self)
            if link[1] == 2:
                link[0].send(routerPacket, self)


    def generateACKRouterPacket(self, packet):
        '''
            Generate ACK for Router packet received and calculate the time cost
            
            Args:
                packet: the packet received
        '''
        neigh = packet.source.address
        comeCost = self.engine.getCurrentTime() - packet.timestamp
        ackRouterPacket = RouterPacket(self, self.engine.getCurrentTime(), PACKET_SIZE, comeCost, 'ack_request')
        self.send(neigh, ackRouterPacket)


    def send(self, destAddr, packet):
        '''
            Send out packet
            
            Args:
                destAddr: the IP address of destination
                packet: the packet to be sent
        '''      
        for link in self.links:
            if link[1] == 1:
                if link[0].node2.address == destAddr:
                    link[0].send(packet, self)
#                     self.packet.setPreHop(self, self.engine.getCurrentTime())
                    break
            if link[1] == 2:
                if link[0].node1.address == destAddr:
                    link[0].send(packet, self)
#                     self.packet.setPreHop(self, self.engine.getCurrentTime())
                    break 

 
    def react_to_packet_receipt(self, event):
        '''
            React to packet receipt according to the packet type:
                1) Data Packet: 
                       Call self.receiveData
                2) Router Packet - 'request':
                       Call self.generateACKRouterPacket
                3) Router Packet - 'ack_request':
                       Call self.measureCost
                4) Router Packet - 'update':
                       Call self.updateRT
            
            Args:
                event: event to be reacted to, which should be EVENT_PACKET_RECEIPT here
        '''
        packet = event.packet
        if isinstance(packet, DataPacket):
            self.receiveData(packet)
            
        if isinstance(packet, RouterPacket):
            if packet.type == 'request':
                self.generateACKRouterPacket(packet)
            if packet.type == 'ack_request':
                self.measureCost(packet)
            if packet.type == 'update':
                self.updateRT(packet)

    
    def startMeasureCost(self):
        '''
            Called periodically to for cost measuring
        '''
        
        self.broadcastRequestPacket()

        
    def measureCost(self, packet):
        '''
           Handle receipt of Router Packet - 'ack_request'
           Call  self.broadcastRequestPacket
        '''
        
        neiCost = packet.routerTable
        
        updateVal = (neiCost, packet.source.address)
        self.rt[packet.source.address] = updateVal
        self.broadcastRouterPacket()


    def updateRT(self, neiPacket):
        '''
            Update the Routing Table using dynamic route distance metric
            
            Args:
                neiPacket: the 'update' packet
            In the following comment, "nei" is the neighbor router which sends this update packet to self
        '''
        neiRT = neiPacket.routerTable
        neiCost = self.rt[neiPacket.source.address][0]
        flag = False
        for (destAddr, neiVal) in neiRT.items():
            # fix a cycle routing bug here. If destination address is the router itself, it indicates
            # this is a cycle routing--simply ignore it
            if destAddr == neiPacket.source.address or destAddr == self.address:
                continue
            # if record already exists, check if it is necessary to update 
            if destAddr in self.rt:
                # if nexthop is nei itself, update routing table
                if self.rt[destAddr][1] == neiPacket.source.address:
                    updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                    
                    if self.rt[destAddr] != updateVal:
                        
                        flag = True
                        self.rt[destAddr] = updateVal 
                else:
                    # if nexthop is not nei, change it to nei if the dynamic metric to go through nei is smaller
                    # than the original cost
                    if neiVal[0] + neiCost < self.rt[destAddr][0]:
                        flag = True
                        updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                        self.rt[destAddr] = updateVal
            
            # if this is a new record, add it to routing table           
            else:
                flag = True
                updateVal = (neiVal[0]+neiCost, neiPacket.source.address)
                self.rt[destAddr] = updateVal
        #flag is set to True when routing table changes. 
        if flag:
            # broadcast Router packet with 'update' type to all neighbor routers
            self.broadcastRouterPacket()
        #print out routing table to check network status. use Router1 as a sample
        if self.name == 'R1':
            print self.rt


    def receiveData(self, packet):
        '''
           Handle receipt of Data Packet, send to the next hop
        '''

        if packet.destination.address in self.rt:
            nextHop = self.rt[packet.destination.address][1]   
            self.send(nextHop, packet)
        else:
            self.send(self.links[0], packet)


    def react_to_routing_table_update(self, event):
        '''
            Update the routing table periodically
            Call self.startMeasureCost()
            
            Args:
                event: event to be reacted to, which should be EVENT_ROUTINGTABLE_OUTDATED here            
        '''
        self.startMeasureCost()
        event = Event(self.engine.getCurrentTime() + self.updateTime, self, EVENT_ROUTINGTABLE_UPDATE)
        self.engine.push_event(event)



class Flow(Element):
    '''
        Flow is a TCP level control for data transmission
        
        Attributes:
            engine: engine associated, used for simulation
            name: a specific name
            source: the source host of current packet
            destination: the destination host of current packet
            amount: the total amount of packets
            start_time: start time of current flow
            tcp: the TCP algorithm to be used (which will be specified in parse.py)
            outOfOrderPackets: IF of packets received in advance of the packet expected
            lastOrderedPacketID: ID of the next packet to be expected
    '''
    def __init__(self, engine, name, source, destination, amount, start_time, tcp):
        super(Flow, self).__init__(engine, name)
        self.source = source
        self.destination = destination
        self.amount = amount
        self.start_time = start_time

        self.outOfOrderPackets = []
        self.lastOrderedPacketID = 0
                
        source.addFlow(self)
        destination.addFlow(self)
        self.tcp = tcp
        self.tcp.setFlow(self)


    def generatePacket(self, pck_id):
        '''
            Generate new packet
            
            Args:
                pck_id: the id of the packet to be generated
        '''
        packet = DataPacket(self.source, self.destination, self, self.engine.getCurrentTime(), PACKET_SIZE, 
                            False, pck_id)        
        return packet

        
    def generateAckPacket(self, packet):
        '''
            Generate ACK packet
            1) If packet.pck_id == self.lastOrderedPacketID+1, the packet is the packet to be expected
               else, push the pck_id to the out of order queue
            2) Generate ACK packet with the lastOrderedPacketID
            3) set the same timestamp for the ACK Packet as the original Data Packet
            
            Args:
                packet: the Data Packet received
        '''
        if packet.pck_id <= self.lastOrderedPacketID:
            pass
        else:
            if packet.pck_id == self.lastOrderedPacketID+1:
                self.lastOrderedPacketID += 1
                
                while self.outOfOrderPackets and self.outOfOrderPackets[0] == self.lastOrderedPacketID+1:
                    heapq.heappop(self.outOfOrderPackets)
                    self.lastOrderedPacketID +=1
            else:
                heapq.heappush(self.outOfOrderPackets, packet.pck_id)

        ack_packet = DataPacket(packet.destination, packet.source, self, self.engine.getCurrentTime(), ACK_PACKET_SIZE, 
                                True, self.lastOrderedPacketID + 1)
        ack_packet.setOriginalPacketTimestamp(packet.timestamp)

        return ack_packet

        
    def sourceSend(self, packet):
        '''
            Send new packet from the source node
            
            Args:
                packet: packet to be sent
        '''
        self.source.send(packet)

        
    def destinationSend(self, packet):
        '''
            Send new packet from the destination node
            
            Args:
                packet: packet to be sent
        '''
        self.destination.send(packet)

    
    def sourceReceive(self, packet):
        '''
            Receive packet in the source node, which should be a ACK Packet
            Call TCP to handle it
            
            Args:
                packet: packet received
        '''
        if packet.acknowledgement == True:
            self.tcp.react_to_ack(packet)
    
    def destinationReceive(self,packet): 
        '''
            Receive packet in the destination node, which should be a Data Packet
                1) Call self.generateAckPacket to generate ACK Packet
                2) Send out ACK Packet from the destination node
                3) Calculate packet delay
            
            Args:
                packet: packet received
        '''     
        ack_packet = self.generateAckPacket(packet)
        self.destinationSend(ack_packet)
        # flowrate = 9.4 not 10 because the linkrate is used for data packet and ack packet.
        # Flow rate is the linkrate used for data packet. Datapacketsize/DatapacketSize+ ackPacketSize = 1024/1088*10
        self.engine.recorder.record_flow_rate(self, self.engine.getCurrentTime(), packet.packetsize * 8.0 / 1024 / 1024)
        packet_delay = self.engine.getCurrentTime() - packet.timestamp
       
        self.engine.recorder.record_packet_delay(self, self.engine.getCurrentTime(), packet_delay)


    def react_to_time_out(self, event):
        '''
            Call TCP to handle packet time out 
            
            Args:
                event: event to be reacted to, which should be EVENT_PACKET_TIMEOUT here
        '''   
        self.tcp.react_to_time_out(event)

    
    def react_to_flow_start(self, event):
        '''
            Call TCP to handle Flow Start

            
            Args:
                event: event to be reacted to, which should be EVENT_FLOW_START here
        '''   
        self.tcp.react_to_flow_start(event)




