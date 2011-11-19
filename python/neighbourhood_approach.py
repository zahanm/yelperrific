from create_matrices import *
from math import sqrt
import heapq

edges = {}
business_edges = {}

def neighbourhood_approach(training_matrix, user_dict, business_dict,
                           test_file, k=5):
    global edges
    f = gzip.open(test_file, 'rb')
    lines = f.readlines()
    f.close()

    error, total = 0.0, 0.0
    n_users, n_businesses = training_matrix.shape
    for line in lines:
        record = json.loads(line)
        if record['type'] == 'review':
            user_id = record['user_id']
            business_id = record['user_id']

            if user_id not in user_dict:
                continue
            if business_id not in business_dict:
                continue
            
            user_i = user_dict[user_id]
            business_i = business_dict[business_id]

            user_row = training_matrix.getrow(user_i)
            knn = []
            
            for i in range(n_users):
                if i == user_i:
                    continue

                if (user_i, i) in edges:
                    value = edges[(user_i, i)]
                elif (i, user_i) in edges:
                    value = edges[(i, user_i)]
                else:
                    value = cosine_similarity(training_matrix, user_i, i)
                    edges[(user_i, i)] = value

                if value > 0:
                    heapq.heappush(knn, (i, value))
                    
            top_k = heapq.nlargest(k, knn, key=lambda x: x[1])
            prediction = sum(training_matrix[i, business_i] for i in \
                             top_k) / k



def item_approach(training_matrix, user_dict, business_dict, test_file, k=1):
    global business_edges
    f = gzip.open(test_file, 'rb')
    lines = f.readlines()
    f.close()

    error, total = 0.0, 0.0
    n_users, n_businesses = training_matrix.shape
    for line in lines:
        record = json.loads(line)
        if record['type'] == 'review':
            user_id = record['user_id']
            business_id = record['business_id']

            if user_id not in user_dict:
                continue

            if business_id not in business_dict:
                continue

            user_i = user_dict[user_id]
            business_i = business_dict[business_id]

            user_row = training_matrix.getrow(user_i)
            business_col = training_matrix.getcol(business_i)

            other_ratings = user_row.nonzero()[1]
            knn = []

            for o_business in other_ratings:
                if business_i == o_business:
                    continue

                if (business_i, o_business) in business_edges:
                    value = business_edges[(business_i, o_business)]
                if (o_business, business_i) in business_edges:
                    value = business_edges[(o_business, business_i)]
                else:
                    value = cosine_similarity(training_matrix, o_business, business_i, use_row=False)
                    business_edges[(business_i, o_business)] = value

                if value > 0.0:
                    heapq.heappush(knn, (o_business, value))
                    
            top_k = heapq.nlargest(k, knn, key=lambda x: x[1])
            prediction = sum(training_matrix[user_i, i] for (i, rating) in \
                             top_k) / float(k)

            if prediction > 0:
                prediction = 4.0
                actual_val = record['stars']
                square_diff = (prediction - actual_val) ** 2
                error += square_diff
                total += 1

    error = sqrt(error) / total
    return error


def cosine_similarity(training_matrix, item_a, item_b, use_row=True):
    if use_row:
        vec_a = training_matrix.getrow(item_a)
        vec_b = training_matrix.getrow(item_b)

    else:
        vec_a = training_matrix.getcol(item_a).getH()
        vec_b = training_matrix.getcol(item_b).getH()

    dot_prod = vec_a.dot(vec_b.getH())[0, 0]
    mag_a = vec_a.dot(vec_a.getH())[0, 0]
    mag_b = vec_b.dot(vec_b.getH())[0, 0]

    return dot_prod / sqrt(mag_a * mag_b)
        

if __name__ == '__main__':
    train_file = 'data/dev-train.json.gz'
    matrix, user_dict, business_dict = create_user_business_matrix(train_file)
    error = item_approach(matrix, user_dict, business_dict, 'data/dev-test.json.gz')
