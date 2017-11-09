# Loads data structures from disk
from nltk.probability import FreqDist
import os
import json 
import re

words_dictionary = []
occ = FreqDist()
frequencies = []

with open(os.path.join(os.path.dirname(__file__), 'words_dictionary.json')) as data_file:    
    words_dictionary = json.load(data_file)

for word in words_dictionary:
    onset = re.findall('^[bcdfghjklmnpqrstvwxz]{1,}', word)
    if len(onset) > 0:
        occ[onset[0]] += 1

with open(os.path.join(os.path.dirname(__file__), 'freq.json')) as f:
    frequencies = json.loads(f.read())