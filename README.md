# cs143_final

This is project code for CS143, which realizes network simulation.

Element.py includes definition for host, packet, link, router, flow.

Event.py defines each event, which works like callback to call the reactor run specific function.

Engine.py is a priority queue which schedules each event one by one during simulation process.

Parse.py will read in the network structure(testcase in txt file) then create network element based on the input.

Record.py works like logger, which records important network parameters(flow rate, packet loss,etc) while simulation.

To begin the simulation, Run testcase.py 
    1. Change test case: Set CURRENT_TEST in testcase.py to 0, 1 or 2.
    2. Change TCP: Set different tcp protocal in parse.py (Line 89).

Data Visulization. we provide two ways to display the plot.
    1. Use the plot function in record.py(detailed plot, used when you need to have a close look of how every link/router works)
    2. Use the corresponding dataPlot_testcase%.m file for better performance.(overall plot, better to use when you want to 
    see how links/router interact with each other in a network)
