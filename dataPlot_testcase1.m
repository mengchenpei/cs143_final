% For Test Case 1

clc;
close all;
clear all;

%% Initialization
dir = 'simu_data/data_reno_testcase1/';
dirImg = 'img_matlab/';

% F1
for i = 1 : 1
    Flow_flow_rate{i} = [dir, 'F', int2str(i), '_flow_rate', '.txt'];
    Flow_packet_delay{i} = [dir, 'F', int2str(i), '_packet_delay', '.txt'];
    Flow_window_size{i} = [dir, 'F', int2str(i), '_window_size', '.txt'];
end

% L0 - L5
for i = 1 : 6
    Link_link_rate{i} = [dir, 'L', int2str(i - 1), '_link_rate', '.txt'];
end

% L0a, L0b - L5a, L5b
for i = 1 : 6
    Link_a_buffer_occupancy{i} = [dir, 'L', int2str(i - 1), 'a_buffer_occupancy', '.txt'];
    Link_b_buffer_occupancy{i} = [dir, 'L', int2str(i - 1), 'b_buffer_occupancy', '.txt'];
    
    Link_a_packet_loss{i} = [dir, 'L', int2str(i - 1), 'a_packet_loss', '.txt'];
    Link_b_packet_loss{i} = [dir, 'L', int2str(i - 1), 'b_packet_loss', '.txt'];
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

data_link_rate = cell(6, 2);
for i = 1 : 6
    data1 = importdata(Link_link_rate{i});

    data_link_rate{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_rate{i, 2} = data1(1 : size(data1, 1) - 1, 2);   
end

data_link_a = cell(6, 4);
for i = 1 : 6
    data1 = importdata(Link_a_buffer_occupancy{i});
    data2 = importdata(Link_a_packet_loss{i});

    data_link_a{i, 1} = data1(1 : size(data1, 1) - 1, 1);
    data_link_a{i, 2} = data1(1 : size(data1, 1) - 1, 2);
    
    data_link_a{i, 3} = data2(1 : size(data2, 1) - 1, 1);
    data_link_a{i, 4} = data2(1 : size(data2, 1) - 1, 2);
end

data_link_b = cell(6, 4);
for i = 1 : 6
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
h1 = plot(data_link_rate{2, 1}, data_link_rate{2, 2}, 'k.');
h1 = plot(data_link_rate{3, 1}, data_link_rate{3, 2}, 'r.');
legend('L1', 'L2', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'link rate'; '(Mbps)'});
xlim([0 30]);

subplot(6, 1, 2);
hold on;
h1 = plot(data_link_a{2, 1}, data_link_a{2, 2}, 'k.');
h1 = plot(data_link_a{3, 1}, data_link_a{3, 2}, 'r.');
legend('L1 a', 'L2 a', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'buffer occu'; '(pkts)'});
xlim([0 30]);

subplot(6, 1, 3);
hold on;
h1 = plot(data_link_a{2, 3}, data_link_a{2, 4}, 'k.');
h1 = plot(data_link_a{3, 3}, data_link_a{3, 4}, 'r.');
legend('L1 a', 'L2 a', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet loss'; '(pkts)'});
xlim([0 30]);

% subplot(6, 1, 2);
% hold on;
% h1 = plot(data_link_b{2, 1}, data_link_b{2, 2}, 'k.');
% h1 = plot(data_link_b{3, 1}, data_link_b{3, 2}, 'r.');
% legend('L1 b', 'L2 b');
% xlabel('time (s)');
% ylabel('buffer occu');
% xlim([0 20]);
% 
% subplot(6, 1, 3);
% hold on;
% h1 = plot(data_link_b{2, 3}, data_link_b{2, 4}, 'k.');
% h1 = plot(data_link_b{3, 3}, data_link_b{3, 4}, 'r.');
% legend('L1 b', 'L2 b');
% xlabel('time (s)');
% ylabel('packet loss');
% xlim([0 20]);

subplot(6, 1, 4);
hold on;
h1 = plot(data_flow{1, 1}, data_flow{1, 2}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'flow rate'; '(Mbps)'});
xlim([0 30]);

subplot(6, 1, 5);
hold on;
h1 = plot(data_flow{1, 5}, data_flow{1, 6}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'window size'; '(pkts)'});
xlim([0 30]);

subplot(6, 1, 6);
hold on;
h1 = plot(data_flow{1, 3}, data_flow{1, 4}, 'k.');
legend('flow 1', 'Location', 'NorthEastOutside');
xlabel('time (s)');
ylabel({'packet delay'; '(s)'});
xlim([0 30]);

saveas(h1, [dirImg, 'fig_stat', '.png']);

%% Plot Seperate
figure;
hold on;
h1 = plot(data_link_rate{2, 1}, data_link_rate{2, 2}, 'k.');
h1 = plot(data_link_rate{3, 1}, data_link_rate{3, 2}, 'r.');
legend('L1', 'L2');
xlabel('time (s)');
ylabel('link rate (Mbps)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_link_rate', '.png']);

figure;
hold on;
h1 = plot(data_link_a{2, 1}, data_link_a{2, 2}, 'k.');
h1 = plot(data_link_a{3, 1}, data_link_a{3, 2}, 'r.');
legend('L1 a', 'L2 a');
xlabel('time (s)');
ylabel('buffer occupancy (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_buffer_occupancy_a', '.png']);

figure;
hold on;
h1 = plot(data_link_a{2, 3}, data_link_a{2, 4}, 'k.');
h1 = plot(data_link_a{3, 3}, data_link_a{3, 4}, 'r.');
legend('L1 a', 'L2 a');
xlabel('time (s)');
ylabel('packet loss (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_packet_loss_a', '.png']);

figure;
hold on;
h1 = plot(data_link_b{2, 1}, data_link_b{2, 2}, 'k.');
h1 = plot(data_link_b{3, 1}, data_link_b{3, 2}, 'r.');
legend('L1 b', 'L2 b');
xlabel('time (s)');
ylabel('buffer occupancy (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_buffer_occupancy_b', '.png']);

figure;
hold on;
h1 = plot(data_link_b{2, 3}, data_link_b{2, 4}, 'k.');
h1 = plot(data_link_b{3, 3}, data_link_b{3, 4}, 'r.');
legend('L1 b', 'L2 b');
xlabel('time (s)');
ylabel('packet loss (pkts)');
xlim([0 25]);
saveas(h1, [dirImg, 'fig_packet_loss_b', '.png']);

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
