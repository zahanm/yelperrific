
from mrjob.job import MRJob

class BusinessFeatures(MRJob):
  '''
  Calculates a feature vector for each business from the reviews corresponding
  to the business
  '''

  DEFAULT_INPUT_PROTOCOL = 'json_value'

  emit_types = frozenset('review', 'business')

  def mapper(self, _, data):
    if data['type'] in emit_types:
      yield data['business_id'], data
  
  def reducer(self, business_id, data_blobs):
    features = {}
    # initialize features
    features['stars'] = 0
    features['categories'] = []
    features['tot_useful'] = 0
    features['tot_funny'] = 0
    features['tot_cool'] = 0
    # calculate feature vector here
    for data in data_blobs:
      if data['type'] == 'business':
        # there should be only one business object
        features['stars'] = data['stars']
        features['categories'] = data['categories']
      else:
        # add to respective vectors
        features['tot_useful'] += data['votes']['useful']
        features['tot_funny'] += data['votes']['funny']
        features['tot_cool'] += data['votes']['cool']
    yield business_id, features

if __name__ == '__main__':
  BusinessFeatures.run()

'''
Example business object:
{ "city": "Ithaca", "review_count": 35, "name": "Taste of Thai Express", "neighborhoods": [],
  "url": "http://www.yelp.com/biz/taste-of-thai-express-ithaca", "type": "business",
  "business_id": "7FD_ny67bnS6Zm3oa104VA", "full_address": "209 S Meadow St\nIthaca, NY 14850",
  "latitude": 42.437719, "state": "NY", "longitude": -76.5079669, "stars": 3.5,
  "schools": ["Cornell University"], "open": true, "categories": ["Thai", "Restaurants"],
  "photo_url": "http://s3-media4.px.yelpcdn.com/bphoto/LseH1vmVhmWxcxKwubqwHQ/ms.jpg" }

Example review object:
{"votes": {"funny": 1, "useful": 1, "cool": 1}, "user_id": "iCppbv3C7XvCyzIZnNQ7fg", "review_id": "e0n
SjmM8BObGHCOEm1IAqA", "text": "It was the crappiest day of the year and I needed a warm meal that was 
Picante. I went into the Border Cafe for lunch and the place was dead.  I got a great table by the win
ows and the nice waitress appeared instantly. There were about 4 other tables so she really din't have
 anything else to do. She was nice and brought some watery but good salsa and some excellent chips.  I
 looked over the menu and decided on a enchillada and taco combo.  The chicken toaco was okay not bad 
but the enchillada waschessey and wonderful. I made a really stupid error and ordered a cup of coffee.
  DO NOT ORDER THE COFFEE it sucks but what the fuck was I thinking I was in a tex-mex place.  I guess
 I was expecting sa New Orleans chicory kind of coffe but I got a Boston brown piss in a cup.  Thi was
 the only bad part and it was frankly my own damn fault! The service was great, the food good and not 
overly pricey.  I wish I had re-fried beans but at least they were balck beans the rice was od but i t
hink it was the \"cajun\" element.  I will go back.", "business_id": "pvlM--HZY1a8SqMXiwEz1A", "stars"
: 4, "date": "2009-01-29", "type": "review"}
'''
