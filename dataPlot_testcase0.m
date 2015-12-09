% For Test Case 0

clc;
close all;
clear all;

%% Initialization
dir = 'simu_data/data_fast_testcase0/';
dirImg = 'img_matlab/';

% F1
for i = 1 : 1
    Flow_flow_rate{i} = [dir, 'F', int2str(i), '_flow_rate', '.txt'];
    Flow_packet_delay{i} = [dir, 'F', int2str(i), '_packet_delay', '.txt'];
    Flow_window_size{i} = [dir, 'F', int2str(i), '_window_size', '.txt'];
end

% L1
for i = 1 : 1
    Link_link_rate{i} = [dir, 'L', int2str(i), '_link_rate', '.txt'];
end

% L1a, L1b
for i = 1 : 1
    Link_a_buffer_occupancy{i} = [dir, 'L', int2str(i), 'a_buffer_occupancy', '.txt'];
    Link_b_buffer_occupancy{i} = [dir, 'L', int2str(i), 'b_buffer_occupancy', '.txt'];
    
    Link_a_packet_loss{i} = [dir, 'L', int2str(i), 'a_packet_loss', '.txt'];
    Link_b_packet_loss{i} = [dir, 'L', int2str(i), 'b_packet_loss', '.txt'];
end

%% Import Data
data_flow = cell(1, 6);
for i = 1 : 1
    data1 = importdata(Flow_flow_rate{i});
    data2 = importdata(Flow_packet_delay{i});
    data3 = importdata(Flow_window_size{i});

    data_flow{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_flow{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_flow{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_flow{i, 4} = data2(1 : size(data2, 1) - 1, 2);
 
    data_flow{i, 5} = data3(1 : size(data3, 1) - 1, 1);
    data_flow{i, 6} = data3(1 : size(data3, 1) - 1, 2);
end

data_link_rate = cell(1, 2);
for i = 1 : 1
    data1 = importdata(Link_link_rate{i});

    data_link_rate{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_rate{i, 2} = data1(1 : size(data1, 1) - 1, 2);   
end

data_link_a = cell(1, 4);
for i = 1 : 1
    data1 = importdata(Link_a_buffer_occupancy{i});
    data2 = importdata(Link_a_packet_loss{i});

    data_link_a{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_a{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_link_a{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_link_a{i, 4} = data2(1 : size(data2, 1) - 1, 2);
end

data_link_b = cell(1, 4);
for i = 1 : 1
    data1 = importdata(Link_b_buffer_occupancy{i});
    data2 = importdata(Link_b_packet_loss{i});

    data_link_b{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_b{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_link_b{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_link_b{i, 4} = data2(1 : size(data2, 1) - 1, 2);
end

%% Plot - 6 imgs
figure;
hold on;

subplot(6, 1, 1);
hold on;
h1 = plot(data_link_rate{1, 1}, data_link_rate{1, 2}, 'k.');
legend('L1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'link rate'; '(Mbps)'});
xlim([0 20]);

subplot(6, 1, 2);
hold on;
[AX, h1, h2] = plotyy(data_link_a{1, 1}, data_link_a{1, 2}, data_link_b{1, 1}, data_link_b{1, 2});
legend('L1 a', 'L1 b', 'Location', 'NorthEastOutside');
set(h1, 'linestyle', '.')
set(h2, 'linestyle', '.')
set(AX(1), 'xTick', 0 : 5 : 20);
set(AX(2), 'xTick', 0 : 5 : 20);
set(AX(1), 'xLim', [0 20]);
set(AX(2), 'xLim', [0 20]);
xlabel('time (s)');
ylabel({'buffer occu'; '(pkts)'});
xlim([0 20]);

subplot(6, 1, 3);
hold on;
h1 = plot(data_link_a{1, 3}, data_link_a{1, 4}, 'k.');
h1 = plot(data_link_b{1, 3}, data_link_b{1, 4}, 'r.');
legend('L1 a', 'L1 b', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet loss'; '(pkts)'});
xlim([0 20]);

subplot(6, 1, 4);
hold on;
h1 = plot(data_flow{1, 1}, data_flow{1, 2}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'flow rate'; '(Mbps)'});
xlim([0 20]);

subplot(6, 1, 5);
hold on;
h1 = plot(data_flow{1, 5}, data_flow{1, 6}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'window size'; '(pkts)'});
xlim([0 20]);

subplot(6, 1, 6);
hold on;
h1 = plot(data_flow{1, 3}, data_flow{1, 4}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet delay'; '(s)'});
xlim([0 20]);

saveas(h1, [dirImg, 'fig_stat', '.png']);

%% Plot Seperate
figure;
hold on;
h1 = plot(data_link_rate{1, 1}, data_link_rate{1, 2}, 'k.');
legend('L1');
xlabel('time (s)');
ylabel('link rate (Mbps)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_link_rate', '.png']);

figure;
hold on;
hold on;
h1 = plot(data_link_a{1, 1}, data_link_a{1, 2}, 'k.');
h1 = plot(data_link_b{1, 1}, data_link_b{1, 2}, 'r.');
legend('L1 a', 'L1 b');
xlabel('time (s)');
ylabel('buffer occupancy (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_buffer_occupancy', '.png']);

figure;
hold on;
h1 = plot(data_link_a{1, 3}, data_link_a{1, 4}, 'k.');
h1 = plot(data_link_b{1, 3}, data_link_b{1, 4}, 'r.');
legend('L1 a', 'L1 b');
xlabel('time (s)');
ylabel('packet loss (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_packet_loss', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 1}, data_flow{1, 2}, 'k.');
legend('flow 1');
xlabel('time (s)');
ylabel('flow rate (Mbps)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_flow_rate', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 5}, data_flow{1, 6}, 'k.');
legend('flow 1');
xlabel('time (s)');
ylabel('window size (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_window_size', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 3}, data_flow{1, 4}, 'k.');
legend('flow 1');
xlabel('time (s)');
ylabel('packet delay (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_packet_delay', '.png']);
