from mrjob.job import MRJob

"""
Creates a histogram of business review counts
"""

class BusinessDegreeHist(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'json_value'

    def mapper(self, _, data):
        if data['type'] == 'business':
            yield (data['review_count'], 1)

    def reducer(self, review_count, values):
        yield (review_count, sum(values))

if __name__ == '__main__':
    BusinessDegreeHist().run()
