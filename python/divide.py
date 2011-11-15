
import sys
import json

LARGER_FILE = 'data/larger.json'
SMALLER_FILE = 'data/smaller.json'

def divide(input_file, prob):
  with input_file as inp, LARGER_FILE as larger, SMALLER_FILE as smaller:
    for line in inp:
      obj = json.parse(line)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('usage: ', __file__, '<input_json_file> <probability>')
  else:
    input_file = sys.argv[1]
    prob = sys.argv[2]
    divide(input_file, prob)
