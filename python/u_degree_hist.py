from mrjob.job import MRJob

"""
Creates a histogram of user review counts
"""

class UserDegreeHist(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'json_value'

    def mapper(self, _, data):
        if data['type'] == 'user':
            yield (data['review_count'], 1)

    def reducer(self, review_count, values):
        yield (review_count, sum(values))

if __name__ == '__main__':
    UserDegreeHist().run()
