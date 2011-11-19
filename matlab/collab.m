clear all; close all; clc

k = 1000;

train_data = dlmread('../data/official_train.txt');
train_matrix = sparse(train_data(:, 1), train_data(:, 2), train_data(:, 3));

test_data = dlmread('../data/official_test.txt');
actual_ratings = test_data(:, 3);
predicted_ratings = zeros(size(actual_ratings));

num_test = size(test_data, 1);

% normalization factors
norms = sqrt(sum(train_matrix.^2));

% num_test = 10000;

for i = 1:num_test
    b_id = test_data(i, 1);
    u_id = test_data(i, 2);
        
    % Calculate cosine similarity
    similarity = train_matrix(:, u_id)' * train_matrix;
    similarity = similarity ./ norms;
    similarity = similarity ./ norms(u_id);
    similarity(isnan(similarity)) = 0;
    
    % Sort by similarity
    [sorted_sim, sorted_ids] = sort(similarity, 'descend');
    
    % Remove this user's id
    sorted_ids(sorted_ids == u_id) = [];
    
    
    % choose the top k most similar
    neighbor_ids = sorted_ids(1:k);
    
    % pick only neighbors with rating for the business we want
    neighbor_ratings = full(train_matrix(b_id, neighbor_ids));
    neighbor_ratings(neighbor_ratings == 0) = [];
    if isempty(neighbor_ratings)
        predicted_ratings(i) = 0;
    else
        predicted_ratings(i) = mean(neighbor_ratings);
    end
end

rmse = sqrt(mean(predicted_ratings(1:num_test) - actual_ratings(1:num_test)).^2)
baseline3 = sqrt(mean(3 - actual_ratings).^2)
baseline4 = sqrt(mean(4 - actual_ratings).^2)