# -*- coding: utf-8 -*-

from data.models import Sentence
import sys

input_file = sys.argv[3]
print (input_file)
fp = open(input_file, 'r')

for line in fp.readlines():
    line = line.rstrip('\n')
    s = Sentence(text=line)
    s.save()

print('Success')
