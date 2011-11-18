
import json

target_user_id = ''
business_to_rate_id = ''

user_business_output = ''
business_features_output = ''

class ItemBased:

  def __init__(self):
    self.ranking_style = 'Item based'

  def related_businesses(self):
    with open(user_business_output) as ub_output:
      ub = json.load(ub_output)
      return set(ub['target_user_id'])

if __name__ == '__main__':
  ib = ItemBased()
  ib.run()
