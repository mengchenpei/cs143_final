'''
    Simulation Engine (Event Priority Queue)
'''

import heapq
import record


class SimEngine:
    '''
        Main class for network simulation
        
        Attributes:
            queue: event priority queue
            MAXTIME: maximum time for simulation
            curTime: current simulation time stamp
            recorder: handle all data need to be logged and plotted
    '''
    def __init__(self, maxtime):
        self.queue = []
        self.MAXTIME = maxtime
        self.curTime = 0
        self.recorder = record.Record()
        
    def getCurrentTime(self):
        '''
            Get current simulation time
        '''
        return self.curTime

    def push_event(self, event):
        '''
            Push (event.time, event), so that it will be ordered by event.time
            
            Args:
                event: the event to be handled
        '''
        heapq.heappush(self.queue, (event.time, event))

    def pop_event(self):
        '''
            Pop the event, with the nearest time stamp.
            (Ordered by event.time in the queue)
        '''
        return heapq.heappop(self.queue)[1]

    def execute_top(self):
        '''
            Pop and execute the top event
        '''
        event = self.pop_event()
        self.curTime = event.time
        event.execute()
            


    def run(self):
        '''
            Run method of engine
                1) ended when executed all events in the queue
                2) ended when current simulation time exceeds MAXTIME
        '''
        while len(self.queue) > 0 and self.curTime < self.MAXTIME:            
            self.execute_top()




