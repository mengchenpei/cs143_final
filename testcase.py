'''
    Main function for network simulation
'''
from events import * 
from element import  *
from engine import *
from parse import *
import record
import matplotlib.pyplot as plt
import tcp_fast
import tcp_reno

# specify the testcast number: 0, 1 or 2
CURRENT_TEST = 1

# specify the file name for img output
DIR_IMG = 'img_testcase' + str(CURRENT_TEST) + '/'

# specify the file name for data output
DIR_DATA = 'simu_data/data_fast_testcase1/'


def main():
    #initialize engine and set maximum running time 
    #for testcase0/1, the maximun running time is 30, for testcase2, it is 60
    engine = SimEngine(60)
    
    file_name = 'testcase' + str(CURRENT_TEST) + '.txt'

    # parse .txt file and set up the simulation environment
    parse(engine, file_name)
    
    # run the simulation
    engine.run()
    
    #save data output into file, use file to plot        
    for name, inventory in engine.recorder.category[CATE_LINK_RATE].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)
        
        tempFile = DIR_DATA + name + '_link_rate.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))

    for name, inventory in engine.recorder.category[CATE_BUFFER_OCCUPANCY].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)

        tempFile = DIR_DATA + name + '_buffer_occupancy.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
                
    for name, inventory in engine.recorder.category[CATE_PACKET_LOSS].items():
        tempSmooth = engine.recorder.smooth1(0.2, inventory)
        tempSmooth = engine.recorder.smooth2(tempSmooth)
        
        tempFile = DIR_DATA + name + '_packet_loss.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
            
    for name, inventory in engine.recorder.category[CATE_FLOW_RATE].items():
        tempSmooth = engine.recorder.smooth1(0.2, inventory)
        tempSmooth = engine.recorder.smooth2(tempSmooth)
        
        tempFile = DIR_DATA + name + '_flow_rate.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
                                    
    for name, inventory in engine.recorder.category[CATE_WINDOW_SIZE].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)
        
        tempFile = DIR_DATA + name + '_window_size.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
                        
    for name, inventory in engine.recorder.category[CATE_PACKET_DELAY].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)
        
        tempFile = DIR_DATA + name + '_packet_delay.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
            
    for name, inventory in engine.recorder.category[CATE_PKTS_RECEIVED].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)
        
        tempFile = DIR_DATA + name + '_pkts.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))   
            
    for name, inventory in engine.recorder.category[CATE_SSTHRE].items():
        tempSmooth = engine.recorder.smooth(0.2, inventory)
        
        tempFile = DIR_DATA + name + '_ssthre.txt'
        myFile = open(tempFile, 'w')
        for x,y in tempSmooth:
            myFile.write('{} {}\n'.format(x, y))
            
    # Data Visualization   
    engine.recorder.plot()


if __name__ == '__main__':
    main()




