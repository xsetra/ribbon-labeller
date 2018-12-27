# -*- coding: utf-8 -*-

from data.models import Sentence
import sys

input_file = sys.argv[3]
company = sys.argv[4]
sector = sys.argv[5]
print(input_file)

fp = open(input_file, 'r')

for line in fp.readlines():
    line = line.rstrip('\n')
    s = Sentence(text=line, company=company, sector=sector)
    s.save()

print('Success')
