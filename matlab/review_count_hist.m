% Generate histograms of user review count and business review count
clear all; close all; clc;

%% User plot
u_data = dlmread('../data/user_degree.txt');
[u_keys, idx] = sort(u_data(:,1));
u_values = u_data(idx,2);

figure;
loglog(u_keys, u_values);
title('Distribution of user review counts');
xlabel('Review count');
ylabel('Number of users');
hold off;

%% Business plot
b_data = dlmread('../data/business_degree.txt');
[b_keys, idx] = sort(b_data(:,1));
b_values = b_data(idx, 2);

figure;
loglog(b_keys, b_values);
title('Distribution of busines review counts');
xlabel('Review count');
ylabel('Number of businesses');

%% Get mean of datasets
user_mean = (u_keys' * u_values) / sum(u_values)
business_mean = (b_keys' * b_values) / sum(b_values)