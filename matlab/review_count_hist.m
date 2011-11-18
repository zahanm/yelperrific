% Generate histograms of user review count and business review count
clear all; close all; clc;

%% User plot
u_degrees = dlmread('../data/u_degree.out', '\t', 0, 1);
u_edges = sort(unique(u_degrees));
u_hist = hist(u_degrees, u_edges);

figure;
loglog(u_edges, u_hist);
title('Distribution of user review counts');
xlabel('Review count');
ylabel('Number of users');
hold off;

%% Business plot

b_degrees = dlmread('../data/b_degree.out', '\t', 0, 1);
b_edges = sort(unique(b_degrees));
b_hist = hist(b_degrees, b_edges);

figure;
loglog(b_edges, b_hist);
title('Distribution of busines review counts');
xlabel('Review count');
ylabel('Number of businesses');

%% Get mean of datasets
user_mean = mean(u_degrees)
user_med = median(u_degrees)
user_std = std(u_degrees)

business_mean = mean(b_degrees)
business_med = median(b_degrees)
business_std = std(b_degrees)