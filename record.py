from constants import *
import matplotlib.pyplot as plt
import __main__
import collections
from testcase import DIR_IMG


class Record(object):
    '''
        record all the data and plot them
        
        Attributes:
            category: structure to store all the data, sorted by Object name
            unit_string: name of different kinds of data
            unit_smooth: smooth method of different kinds of data
    '''
    def __init__(self):
        self.category = {}
        # set up x-lable and y-lable for each plot
        self.unit_string = {
            CATE_LINK_RATE: ('Time / s', 'Link Rate / Mbps'),
            CATE_PACKET_LOSS: ('Time / s', 'Packet Loss / pkts'), 
            CATE_BUFFER_OCCUPANCY: ('Time / s', 'Buffer Occupancy / pkts'), 
            CATE_FLOW_RATE: ('Time / s', 'Flow Rate / Mbps'), 
            CATE_WINDOW_SIZE: ('Time / s', 'Window Size / pkts'), 
            CATE_PACKET_DELAY: ('Time / s', 'Packet Delay / s'), 
            
            CATE_PKTS_RECEIVED: ('Time / s', 'Packets Received / pkts'),
            CATE_SSTHRE: ('Time / s', 'SSThre / pkts'), 
            CATE_RTT: ('Time / s', 'RTT / s'),
            CATE_STATE : ('Time / s', 'State'),
            CATE_DUP_TIMES : ('Time / s', 'Duplicate Times'),
            CATE_TIMEOUT : ('Time / s', 'Packet Time Out / s') 
              
        }
        #set up smooth function for each plot. Flow_rate and packet_loss use different smooth function from others
        self.unit_smooth = {
            CATE_LINK_RATE: self.smooth,
            CATE_PACKET_LOSS: self.smooth1, 
            CATE_BUFFER_OCCUPANCY: self.smooth, 
            CATE_FLOW_RATE: self.smooth1, 
            CATE_WINDOW_SIZE: self.smooth, 
            CATE_PACKET_DELAY: self.smooth,
             
            CATE_PKTS_RECEIVED: self.smooth,
            CATE_SSTHRE: self.smooth, 
            CATE_RTT: self.smooth,
            CATE_STATE : self.smooth,
            CATE_DUP_TIMES : self.smooth,
            CATE_TIMEOUT: self.smooth
        }
        for cate in CATE_ALL:
            self.category[cate] = {}

    def recordEvent(self, cate, element, time, value):
        '''
            Record event
            
            Args:
                cate: Object name
                element: Type of Object
                time: time stampe
                value: value
        '''
        if element.name not in self.category[cate]:
            
            self.category[cate][element.name] = [(0, 0)]
        content = self.category[cate][element.name]
        content.append((time, value))
        
    def record(self, cate, element, time, value):
        '''
            Record data
            
            Args:
                cate: Object name
                element: Type of Object
                time: time stampe
                value: value
        '''
        if element.name not in self.category[cate]:
            
            self.category[cate][element.name] = [(0, 0)]
        content = self.category[cate][element.name]
        if content[-1][0] != time:
            if content[-1][1] == value:
                pass
            else:
                content.append((time,content[-1][1]))
                content.append((time,value))
        else:
            if content[-1][1] == value:
                pass
            else:
                if len(content) <= 1:
                    content.append((time,value))
                else:
                    if value != content[-2][1]:
                        content.append((time,value))
                    else:
                        content.pop()
                        content.append((time,value))

                
    '''
        All the followings are log functions for different kinds of data
    '''
    def record_link_rate(self, element, time, linkrate): 
        self.record(CATE_LINK_RATE, element, time, linkrate)

        
    def record_flow_rate(self, element, time, flowrate): 
        self.recordEvent(CATE_FLOW_RATE, element, time, flowrate)

        
    def record_packet_delay(self, element, time, packetdelay): 
        self.record(CATE_PACKET_DELAY, element, time, packetdelay)

      
    def record_packet_loss(self, element, time, packetloss): 
        self.recordEvent(CATE_PACKET_LOSS, element, time, packetloss)

        
    def record_buffer_occupancy(self, element, time,bufferoccupancy): 
        self.record(CATE_BUFFER_OCCUPANCY, element, time, bufferoccupancy)

           
    def record_window_size(self, element, time, window_size): 
        self.record(CATE_WINDOW_SIZE, element, time, window_size) 


    def record_pkts_received(self, element, time, pkts_received): 
        self.record(CATE_PKTS_RECEIVED, element, time, pkts_received)

         
    def record_ssthre(self, element, time, threshold): 
        self.record(CATE_SSTHRE, element, time, threshold) 

        
    def record_rtt(self, element, time, RTT): 
        self.record(CATE_RTT, element, time, RTT) 


    def record_state(self, element, time, state): 
        self.record(CATE_STATE, element, time, state) 


    def record_dup_times(self, element, time, dup_times): 
        self.record(CATE_DUP_TIMES, element, time, dup_times) 

        
    def record_timeout(self, element, time, tempTimeOut): 
        self.record(CATE_TIMEOUT, element, time, tempTimeOut) 

    
    '''
        All the followings are several plot method based on matplotlib
    '''
    def draw(self, content, plot_n, title, file_name, xlabel, ylabel):

        x,y = zip(*content)
        
        plt.figure(plot_n)
        plt.plot(x,y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        file_name = DIR_IMG + file_name
        plt.savefig(file_name)
    

    def draw_minmax(self, content, plot_n, title, file_name, xlabel, ylabel, ymin, ymax):
        '''
            Plot specifying ymin and ymax
        '''
        x,y = zip(*content)
        
        plt.figure(plot_n)
        plt.plot(x,y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.ylim(ymin, ymax)
        file_name = DIR_IMG + file_name
        plt.savefig(file_name)


    '''
        All the followings are several data smooth methods
    '''        
    def smooth1(self, interval, inventory):
        scale = 8
        i = 1; slideSize = interval/scale
        start = inventory[0][0]; outputList = collections.deque(); finalList = []
        while start + slideSize < inventory[-1][0]:
            count = 0
            while inventory[i][0]< start + slideSize:
                count += inventory[i][1]
                i += 1
            
            outputList.append((start+slideSize/2, count))
            start += slideSize
        
        while len(outputList) >= scale:
            startTime = outputList[0][0]
            endTime = outputList[scale - 1][0]
            s = 0
            for i in xrange(0, scale):
                s += outputList[i][1]
            
            time = (startTime + endTime) / 2
            s = s / interval
            
            finalList.append((time,s))
            outputList.popleft()
        return finalList
    

    def smooth2(self, preSmooth):
        gamma = 0.25; smooth = []; smooth.append(preSmooth[0])
        pre = preSmooth[0][1]
        for i in range(1,len(preSmooth)):
            pre = (1 - gamma) * pre + gamma * preSmooth[i][1]
            smooth.append((preSmooth[i][0], pre))
        return smooth
            
            
    def smooth(self, interval, inventory):
        i = 1
        start = inventory[0][0]
        sumup = 0; avg = 0
        outputList = []
        slideSize = interval/4; 
        while start + interval< inventory[-1][0]:
            sumup = 0
            returnPoint = -1
            while inventory[i][0]< start + interval:
                if inventory[i][0] > start+slideSize:
                    if returnPoint == -1:
                        returnPoint = i
                if inventory[i-1][0] < start:
                    sumup -= (start-inventory[i-1][0]) * inventory[i-1][1]
                sumup += (inventory[i][0] - inventory[i-1][0])* inventory[i-1][1]
                i += 1
            sumup += (start + interval - max(inventory[i-1][0], start))*inventory[i-1][1]
            
            avg = sumup/interval
            outputList.append((start+interval/2, avg))
            
            start += slideSize
            if returnPoint != -1:
                i = returnPoint
        return outputList

    
    def plot(self):
        n = 0
        for cate in self.category:        
            cur_cate = cate
            x_unit, y_unit = self.unit_string[cate]
                        
            for element in self.category[cur_cate]:                
                cur_string = cur_cate + '_' + element     
    
                smooth = self.unit_smooth[cur_cate](0.2, self.category[cur_cate][element])
                if cate == CATE_FLOW_RATE or cate == CATE_PACKET_LOSS:
                    smooth = self.smooth2(smooth)
                print len(smooth)
                 
                if smooth:
                    self.draw(smooth, n, cur_string, cur_string, x_unit, y_unit)
                    n += 1
                else:
                    print 'empty smooth:  ' + cur_string
   
        print 'Imgs Plot: Finished!'
        plt.show()



def main():
    '''
        main function to run the Recorder
    '''
    a = Record()
    a.calAvg()

         
if __name__ == '__main__':
     
    main()




