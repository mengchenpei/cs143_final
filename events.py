from constants import *

class Event:
    '''
        Event defines all events in the simulation
        
        Attributes:
            time: the time event will happen
            reactor: object to handle the event
            packet: the packet to be received
    '''
    def __init__(self, time, reactor, type):
        self.time = time
        self.reactor = reactor
        self.type = type

    def execute(self):
        '''
            Execute corresponding event according to the event type
        '''
        if (self.type == EVENT_LINK_AVAILABLE):
            self.reactor.react_to_link_available(self)
        if (self.type == EVENT_PACKET_RECEIPT):
            self.reactor.react_to_packet_receipt(self)
        if (self.type == EVENT_ROUTINGTABLE_OUTDATED):
            self.reactor.react_to_routing_table_outdated(self)
        if (self.type == EVENT_ROUTINGTABLE_UPDATE):
            self.reactor.react_to_routing_table_update(self)
        if (self.type == EVENT_PACKET_TIMEOUT):
            self.reactor.react_to_time_out(self)
        if (self.type == EVENT_FLOW_START):
            self.reactor.react_to_flow_start(self)
        if (self.type == EVENT_FAST_UPDATE):
            self.reactor.react_fast_update(self)
            
    @staticmethod
    def CreateEventFastUpdate(time, reactor):
        '''
            Create a packet receive event
            
            Args:
                time: the time event will happen
                reactor: object to handle the event
                packet: the packet to be received
        '''
        event = Event(time, reactor, EVENT_FAST_UPDATE)
        
        return event 

    @staticmethod
    def CreateEventPacketReceipt(time, reactor, packet):
        '''
            Create a packet receive event
            
            Args:
                time: the time event will happen
                reactor: object to handle the event
                packet: the packet to be received
        '''
        event = Event(time, reactor, EVENT_PACKET_RECEIPT)
        event.packet = packet
        return event 
    
    @staticmethod
    def CreateEventPacketTimeOut(time, reactor, pck_id=None):
        '''
            Create a packet time_out event
            
            Args:
                time: the time event will happen
                reactor: object to handle the event
                pck_id: ID of the packet which will be time_out
        '''
        event = Event(time, reactor, EVENT_PACKET_TIMEOUT)
        event.pck_id = pck_id
        return event




