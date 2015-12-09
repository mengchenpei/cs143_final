% For Test Case 2

clc;
close all;
clear all;

%% Initialization
dir = 'simu_data/data_reno_testcase2/';
dirImg = 'img_matlab/';

% F1 - F3
for i = 1 : 3
    Flow_flow_rate{i} = [dir, 'F', int2str(i), '_flow_rate', '.txt'];
    Flow_packet_delay{i} = [dir, 'F', int2str(i), '_packet_delay', '.txt'];
    Flow_window_size{i} = [dir, 'F', int2str(i), '_window_size', '.txt'];
end

% L1 - L9
for i = 1 : 9
    Link_link_rate{i} = [dir, 'L', int2str(i), '_link_rate', '.txt'];
end

% L1a, L1b - L9a, L9b
for i = 1 : 9
    Link_a_buffer_occupancy{i} = [dir, 'L', int2str(i), 'a_buffer_occupancy', '.txt'];
    Link_b_buffer_occupancy{i} = [dir, 'L', int2str(i), 'b_buffer_occupancy', '.txt'];
    
    Link_a_packet_loss{i} = [dir, 'L', int2str(i), 'a_packet_loss', '.txt'];
    Link_b_packet_loss{i} = [dir, 'L', int2str(i), 'b_packet_loss', '.txt'];
end

%% Import Data
% F1 - F3
data_flow = cell(3, 6);
for i = 1 : 3
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

% L1 - L9
data_link_rate = cell(9, 2);
for i = 1 : 9
    data1 = importdata(Link_link_rate{i});

    data_link_rate{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_rate{i, 2} = data1(1 : size(data1, 1) - 1, 2);   
end

% L1a, L1b - L9a, L9b
data_link_a = cell(9, 4);
for i = 1 : 9
    data1 = importdata(Link_a_buffer_occupancy{i});
    data2 = importdata(Link_a_packet_loss{i});

    data_link_a{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_a{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_link_a{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_link_a{i, 4} = data2(1 : size(data2, 1) - 1, 2);
end

data_link_b = cell(9, 4);
for i = 1 :9
    data1 = importdata(Link_b_buffer_occupancy{i});
    data2 = importdata(Link_b_packet_loss{i});

    data_link_b{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_b{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_link_b{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_link_b{i, 4} = data2(1 : size(data2, 1) - 1, 2);
end

%% Plot - 6 imgs
xMin = 0;
xMax = 70;

figure;
hold on;

subplot(6, 1, 1);
hold on;
h1 = plot(data_link_rate{1, 1}, data_link_rate{1, 2}, 'k.');
h1 = plot(data_link_rate{2, 1}, data_link_rate{2, 2}, 'r.');
h1 = plot(data_link_rate{3, 1}, data_link_rate{3, 2}, 'g.');
legend('L1', 'L2', 'L3', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'link rate'; '(Mbps)'});
xlim([xMin xMax]);

subplot(6, 1, 2);
hold on;
h1 = plot(data_link_a{1, 1}, data_link_a{1, 2}, 'k.');
h1 = plot(data_link_a{2, 1}, data_link_a{2, 2}, 'r.');
h1 = plot(data_link_a{3, 1}, data_link_a{3, 2}, 'g.');
legend('L1 a', 'L2 a', 'L3 a', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'buffer occu'; '(pkts)'});
xlim([xMin xMax]);

subplot(6, 1, 3);
hold on;
h1 = plot(data_link_a{1, 3}, data_link_a{1, 4}, 'k.');
h1 = plot(data_link_a{2, 3}, data_link_a{2, 4}, 'r.');
h1 = plot(data_link_a{3, 3}, data_link_a{3, 4}, 'g.');
legend('L1 a', 'L2 a', 'L3 a', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet loss'; '(pkts)'});
xlim([xMin xMax]);

% subplot(6, 1, 2);
% hold on;
% h1 = plot(data_link_b{1, 1}, data_link_b{1, 2}, 'k.');
% h1 = plot(data_link_b{2, 1}, data_link_b{2, 2}, 'r.');
% h1 = plot(data_link_b{3, 1}, data_link_b{3, 2}, 'g.');
% legend('L1 b', 'L2 b', 'L3 b');
% xlabel('time (s)');
% ylabel('buffer occu');
% xlim([xMin xMax]);
% 
% subplot(6, 1, 3);
% hold on;
% h1 = plot(data_link_b{1, 3}, data_link_b{1, 4}, 'k.');
% h1 = plot(data_link_b{2, 3}, data_link_b{2, 4}, 'r.');
% h1 = plot(data_link_b{3, 3}, data_link_b{3, 4}, 'g.');
% legend('L1 b', 'L2 b', 'L3 b');
% xlabel('time (s)');
% ylabel('packet loss');
% xlim([xMin xMax]);

subplot(6, 1, 4);
hold on;
h1 = plot(data_flow{1, 1}, data_flow{1, 2}, 'k.');
h1 = plot(data_flow{2, 1}, data_flow{2, 2}, 'r.');
h1 = plot(data_flow{3, 1}, data_flow{3, 2}, 'g.');
legend('flow 1', 'flow 2', 'flow 3', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'flow rate'; '(Mbps)'});
xlim([xMin xMax]);

subplot(6, 1, 5);
hold on;
h1 = plot(data_flow{1, 5}, data_flow{1, 6}, 'k.');
h1 = plot(data_flow{2, 5}, data_flow{2, 6}, 'r.');
h1 = plot(data_flow{3, 5}, data_flow{3, 6}, 'g.');
legend('flow 1', 'flow 2', 'flow 3', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'window size'; '(pkts)'});
xlim([xMin xMax]);
ylim([0 200]);

subplot(6, 1, 6);
hold on;
h1 = plot(data_flow{1, 3}, data_flow{1, 4}, 'k.');
h1 = plot(data_flow{2, 3}, data_flow{2, 4}, 'r.');
h1 = plot(data_flow{3, 3}, data_flow{3, 4}, 'g.');
legend('flow 1', 'flow 2', 'flow 3', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet delay'; '(s)'});
xlim([xMin xMax]);

saveas(h1, [dirImg, 'fig_stat', '.png']);

%% Plot Seperate
figure;
hold on;
h1 = plot(data_link_rate{1, 1}, data_link_rate{1, 2}, 'k.');
h1 = plot(data_link_rate{2, 1}, data_link_rate{2, 2}, 'r.');
h1 = plot(data_link_rate{3, 1}, data_link_rate{3, 2}, 'g.');
legend('L1', 'L2', 'L3');
xlabel('time (s)');
ylabel('link rate (Mbps)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_link_rate', '.png']);

figure;
hold on;
h1 = plot(data_link_a{1, 1}, data_link_a{1, 2}, 'k.');
h1 = plot(data_link_a{2, 1}, data_link_a{2, 2}, 'r.');
h1 = plot(data_link_a{3, 1}, data_link_a{3, 2}, 'g.');
legend('L1 a', 'L2 a', 'L3 a');
xlabel('time (s)');
ylabel('buffer occupancy (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_buffer_occupancy_a', '.png']);

figure;
hold on;
h1 = plot(data_link_a{1, 3}, data_link_a{1, 4}, 'k.');
h1 = plot(data_link_a{2, 3}, data_link_a{2, 4}, 'r.');
h1 = plot(data_link_a{3, 3}, data_link_a{3, 4}, 'g.');
legend('L1 a', 'L2 a', 'L3 a');
xlabel('time (s)');
ylabel('packet loss (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_packet_loss_a', '.png']);

figure;
hold on;
h1 = plot(data_link_b{1, 1}, data_link_b{1, 2}, 'k.');
h1 = plot(data_link_b{2, 1}, data_link_b{2, 2}, 'r.');
h1 = plot(data_link_b{3, 1}, data_link_b{3, 2}, 'g.');
legend('L1 b', 'L2 b', 'L3 b');
xlabel('time (s)');
ylabel('buffer occupancy (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_buffer_occupancy_b', '.png']);

figure;
hold on;
h1 = plot(data_link_b{1, 3}, data_link_b{1, 4}, 'k.');
h1 = plot(data_link_b{2, 3}, data_link_b{2, 4}, 'r.');
h1 = plot(data_link_b{3, 3}, data_link_b{3, 4}, 'g.');
legend('L1 b', 'L2 b', 'L3 b');
xlabel('time (s)');
ylabel('packet loss (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_packet_loss_b', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 1}, data_flow{1, 2}, 'k.');
h1 = plot(data_flow{2, 1}, data_flow{2, 2}, 'r.');
h1 = plot(data_flow{3, 1}, data_flow{3, 2}, 'g.');
legend('flow 1', 'flow 2', 'flow 3');
xlabel('time (s)');
ylabel('flow rate (Mbps)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_flow_rate', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 5}, data_flow{1, 6}, 'k.');
h1 = plot(data_flow{2, 5}, data_flow{2, 6}, 'r.');
h1 = plot(data_flow{3, 5}, data_flow{3, 6}, 'g.');
legend('flow 1', 'flow 2', 'flow 3');
xlabel('time (s)');
ylabel('window size (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_window_size', '.png']);

figure;
hold on;
h1 = plot(data_flow{1, 3}, data_flow{1, 4}, 'k.');
h1 = plot(data_flow{2, 3}, data_flow{2, 4}, 'r.');
h1 = plot(data_flow{3, 3}, data_flow{3, 4}, 'g.');
legend('flow 1', 'flow 2', 'flow 3');
xlabel('time (s)');
ylabel('packet delay (pkts)');
xlim([xMin xMax]);
saveas(h1, [dirImg, 'fig_packet_delay', '.png']);
