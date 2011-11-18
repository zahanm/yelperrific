from mrjob.job import MRJob

"""
Outputs user id -> review count
"""

class UserDegreeHist(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'json_value'

    def mapper(self, _, data):
        if data['type'] == 'review':
            yield (data['user_id'], 1)

    def reducer(self, u_id, values):
        yield (u_id, sum(values))

if __name__ == '__main__':
    UserDegreeHist().run()
