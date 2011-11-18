from mrjob.job import MRJob

"""
Outputs business id -> review count
"""

class BusinessDegreeHist(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'json_value'

    def mapper(self, _, data):
        if data['type'] == 'review':
            yield (data['business_id'], 1)

    def reducer(self, b_id, values):
        yield (b_id, sum(values))

if __name__ == '__main__':
    BusinessDegreeHist().run()
