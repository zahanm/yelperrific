
from __future__ import print_function

import sys
import json
from random import random

LARGER_FILE = 'data/larger.json'
SMALLER_FILE = 'data/smaller.json'

class Divider:

  def __init__(self, input_file, prob=0.1):
    self.input_file = input_file
    self.prob = prob
    self.sm_bus_ids = set()
    self.sm_users_ids = set()

  def reviews_pass(self):
    with open(self.input_file) as inp, open(LARGER_FILE, 'w') as larger, open(SMALLER_FILE, 'w') as smaller:
      for line in inp:
        obj = json.loads(line)
        out = larger
        if obj['type'] == 'review':
          if random() < self.prob:
            out = smaller
            self.sm_bus_ids.add(obj['business_id'])
            self.sm_users_ids.add(obj['user_id'])
        json.dump(obj, out)
        out.write('\n')
    print('Done isolating smaller set')

  def pull_in_related(self):
    with open(self.input_file) as inp, open(SMALLER_FILE, 'a') as smaller:
      for line in inp:
        obj = json.loads(line)
        if obj['type'] == 'business' and obj['business_id'] in self.sm_bus_ids:
          json.dump(obj, smaller)
          smaller.write('\n')
        elif obj['type'] == 'user' and obj['user_id'] in self.sm_users_ids:
          json.dump(obj, smaller)
          smaller.write('\n')

  def run(self):
    self.reviews_pass()
    self.pull_in_related()

  def __str__(self):
    return 'Divider <' + str(self.input_file) + ', ' + str(self.prob) + '>'

if __name__ == '__main__':
  if len(sys.argv) < 2 or len(sys.argv) >= 4:
    print('usage:', __file__, '<input_json_file> <probability>')
  else:
    input_file = sys.argv[1]
    prob = 0.1
    if len(sys.argv) == 3:
      prob = sys.argv[2]
    d = Divider(input_file, prob)
    d.run()
