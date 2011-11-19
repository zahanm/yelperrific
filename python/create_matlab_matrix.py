import json
import gzip

"""
Outputs a text file of a sparse matrix for matlab
"""

class MatrixCreator:
    def __init__(self, input_file):
        self.b_dict = {}
        self.u_dict = {}
        self._createDictionaries(input_file)

    def createMatrix(self, input_file, output_file):
        with gzip.open(input_file) as inp, open(output_file, 'w') as out:
            for line in inp:
                obj = json.loads(line)
                if obj['type'] == 'review':
                    b_id = self.b_dict[obj['business_id']]
                    u_id = self.u_dict[obj['user_id']]
                    rating = obj['stars']
                    out.write('%d\t%d\t%d\n' % (b_id, u_id, rating))


    def _createDictionaries(self, input_file):
        b_id, u_id = 1, 1
        with gzip.open(input_file) as inp:
            for line in inp:
                obj = json.loads(line)
                if obj['type'] == 'business':
                    self.b_dict[obj['business_id']] = b_id
                    b_id += 1
                elif obj['type'] == 'user':
                    self.u_dict[obj['user_id']] = u_id
                    u_id += 1

if __name__ == '__main__':
    all_data = '../data/yelp_academic_dataset.json.gz'
    train_data = '../data/official-train.json.gz'
    test_data = '../data/official-test.json.gz'

    m = MatrixCreator(all_data)
    m.createMatrix(train_data, 'official_train.txt')
    m.createMatrix(test_data, 'official_test.txt')
    
