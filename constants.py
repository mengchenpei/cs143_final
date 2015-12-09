'''
    Constants
'''

'''
    Size of Data Packet and ACK Packet
'''
PACKET_SIZE = 1024
ACK_PACKET_SIZE = 64

'''
    Interval of Routing Table Updating
'''
ROUTER_PACKET_GENERATION_INTERVAL = 5

'''
    Scale factor for log computation
'''
BIT_TO_PKT_SCALOR = 10.0 * 1024 * 1024 / PACKET_SIZE

'''
    The followings are all events need to be handled
'''
EVENT_LINK_AVAILABLE = 'LinkAvailable'
EVENT_PACKET_RECEIPT = 'PacketReceipt'
EVENT_ROUTINGTABLE_OUTDATED = 'RoutingTableOutdated'
EVENT_PACKET_TIMEOUT = 'PacketTimeOut'
EVENT_FLOW_START = 'FlowStart'
EVENT_ROUTINGTABLE_UPDATE = 'RoutingTableUpdate'
EVENT_FAST_UPDATE = 'FastUpdate'

'''
    The followings are all data can be logged and plotted   
'''
CATE_LINK_RATE = "cate_link_rate"
CATE_PACKET_LOSS = "cate_packet_loss"
CATE_BUFFER_OCCUPANCY = "cate_buffer_occupancy"
CATE_FLOW_RATE = "cate_flow_rate"
CATE_WINDOW_SIZE = "cate_window_size"
CATE_PACKET_DELAY = "cate_packet_delay"

CATE_PKTS_RECEIVED = "cate_pkts_received"
CATE_SSTHRE = "cate_ssthre"
CATE_RTT = "cate_rtt"
CATE_STATE = "cate_state"
CATE_DUP_TIMES = "cate_dup_times"
CATE_TIMEOUT = "cate_timeout"

CATE_ALL = [CATE_LINK_RATE, CATE_PACKET_LOSS, CATE_BUFFER_OCCUPANCY, CATE_FLOW_RATE, CATE_WINDOW_SIZE, 
            CATE_PACKET_DELAY, CATE_PKTS_RECEIVED, CATE_SSTHRE, CATE_RTT, CATE_STATE, CATE_DUP_TIMES, CATE_TIMEOUT]




