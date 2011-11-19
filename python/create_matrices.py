from __future__ import print_function
import sys

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')
    else:
        readline.parse_and_bind("tab: complete")

import json
import sys
import gzip
from scipy.sparse import *

def create_user_business_matrix(data_file):
    f = gzip.open(data_file, 'rb')
    lines = f.readlines()
    f.close()

    business_dict, user_dict = {}, {}    
    businesses, users = [], []
    business_i, user_i = 0, 0

    records = []

    for line in lines:
        records.append(json.loads(line))

    for record in records:      
        if record['type'] != 'review':
            continue

        try:
            user_id = record['user_id']
            business_id = record['business_id']
        
            if user_id not in user_dict:
                user_dict[user_id] = user_i
                user_i += 1
                users.append(user_id)
            
            if business_id not in business_dict:
                business_dict[business_id] = business_i
                business_i += 1
                businesses.append(business_id)

        except:
            print(record)

    S = dok_matrix((user_i, business_i))
    for record in records:
        if record['type'] != 'review':
            continue

        try:
            user_id = record['user_id']
            business_id = record['business_id']
            user_i = user_dict[user_id]
            business_i = business_dict[business_id]
            rating = int(record['stars'])
            S[user_i, business_i] = rating

        except:
            pass

    return (S, user_dict, business_dict)

    
if __name__ == '__main__':
    train_file = 'data/dev-train.json.gz'
    matrix, user_dict, business_dict = create_user_business_matrix(train_file)
