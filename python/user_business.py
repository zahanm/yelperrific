
from mrjob.job import MRJob

class UserBusiness(MRJob):
  '''
  Creates a list of all businesses associated with each user
  That is, a list of businesses revied by a user
  '''

  DEFAULT_INPUT_PROTOCOL = 'json_value'

  def mapper(self, _, data):
    if data['type'] == 'review':
      yield data['user_id'], data['business_id']
  
  def reducer(self, user_id, business_ids):
    yield user_id, business_ids

if __name__ == '__main__':
  UserBusiness.run()
