from e2p.assignment8_jacob_goldman import text_to_pig
from p2e.naive import pig_to_text
from nltk.corpus import words as _words,reuters,brown,gutenberg,wordnet,stopwords
from nltk.probability import FreqDist

import json
import re

print('Loading word set...') # two options for our dictionary of english words, one generated from NLTK corpora
# words = set([word.lower() for word in wordnet.words()] + [word.lower() for word in brown.words()] + [word.lower() for word in stopwords.words('english')] + [word.lower() for word in words.words()])
# or this dict with ~30k more (from https://github.com/dwyl/english-words)
with open('words_dictionary.json') as data_file:    
    words = json.load(data_file)

# we generate a frequency distribution of onset consonant clusters to make an educated guess on names and other words not within our word set
b_clust = FreqDist()
for word in words:
    onset = re.findall('^[bcdfghjklmnpqrstvwxz]{1,}', word)
    if len(onset) > 0:
        b_clust[onset[0]] += 1

print('Loading freqdist...')    # We use a frequency distribution created from brown, reuters, stopwords, and nltk's words
# freq = FreqDist( [ word.lower() for word in brown.words()] + [ word.lower() for word in reuters.words()] + [ word.lower() for word in stopwords.words('english')] + [ word.lower() for word in _words.words()])
# takes a while to generate, so we save to freq.json
with open('freq.json', 'r') as f:
    freq = json.loads(f.read())

# We take a text, apply pig_to_text on it and then count averages (excluding punctuation)
print('Pigify and depigify...')
def test_text(text):
    new_text = (pig_to_text(text_to_pig(text), freq, words, b_clust))
    count = 0
    total = 0
    wrong = []
    for i in range(0, len(text)):
        if text[i].isalpha():
            total += 1
            if text[i] == new_text[i]:
                count += 1
            else:
                wrong.append((text[i], new_text[i]))
    print("Accuracy:", count / total)
    print(wrong[0:50])
    print(len(set(wrong)))
    return count/total

#test_text('Hello world!'.split())
#test_text(gutenberg.words('melville-moby_dick.txt'))

# Test all Gutenberg Texts
count = 0
total = 0
for fileid in gutenberg.fileids():
    print(fileid)
    count += test_text(gutenberg.words(fileid))
    total += 1
print(count / total)
# result = 97.773%
# lower than avg mostly due to less success with Shakespeare

# while True:
#     text = input()
#     text = re.sub('[^\w\s]', '', text).split(' ')
#     pig = text_to_pig(text)
#     print(' '.join(pig))
#     print(' '.join( pig_to_text(pig, freq, words, b_clust)))