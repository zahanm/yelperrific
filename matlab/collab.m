clear all; close all;

k = 100;

train_data = dlmread('../data/official_all.txt');
train_matrix = sparse(train_data(:, 1), train_data(:, 2), train_data(:, 3));

test_data = dlmread('../data/official_test.txt');
actual_ratings = test_data(:, 3);
predicted_ratings = zeros(size(actual_ratings));

num_test = size(test_data, 1);

% normalization factors
norms = sqrt(sum(train_matrix.^2));

% num_test = 10000;

for i = 1:num_test
    if (rem(i, 1000) == 0)
        fprintf('Finished %g of %g\n', i, num_test);
    end
    
    b_id = test_data(i, 1);
    u_id = test_data(i, 2);
    gold_rating = test_data(i, 3);
    
    % remove the rating we want to predict from the matrix
    train_matrix(b_id, u_id) = 0;
    
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
    
    
    % pick only neighbors with ratings for the business we want
    neighbor_ratings = full(train_matrix(b_id, neighbor_ids));
    neighbor_ratings(neighbor_ratings == 0) = [];

    if isempty(neighbor_ratings)
        % default -- predict mode
        predicted_ratings(i) = 4;
    else
        predicted_ratings(i) = mean(neighbor_ratings);
    end
    
    % restore the rating
    train_matrix(b_id, u_id) = gold_rating;
end

rmse = sqrt(mean((predicted_ratings - actual_ratings).^2))
baseline3 = sqrt(mean((3 - actual_ratings).^2))
baseline4 = sqrt(mean((4 - actual_ratings).^2))