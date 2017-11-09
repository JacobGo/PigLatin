from to_pig_latin import text_to_pig
from freq_based import pig_to_text
from nltk.corpus import words as _words,reuters,brown,gutenberg,wordnet,stopwords
from nltk.probability import FreqDist

import json
import re

print('Loading word set...') # two options for our dictionary of english words, one generated from NLTK corpora
# words = set([word.lower() for word in wordnet.words()] + [word.lower() for word in brown.words()] + [word.lower() for word in stopwords.words('english')] + [word.lower() for word in words.words()])
# or this dict with ~30k more (from https://github.com/dwyl/english-words)
with open('words_dictionary.json') as data_file:    
    words = json.load(data_file)
print(len(words))
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
        if text[i].isalpha() or True:
            total += 1
            if text[i] == new_text[i]:
                count += 1
            else:
                wrong.append((text[i], new_text[i]))
    print("Accuracy:", count / total)
    print(set(wrong))
    print(len(wrong))
    return count/total

from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()

# test_text('Hello world!'.split())
# # Result: 100%

# test_text(gutenberg.words('melville-moby_dick.txt'))
# # Result: 98.86014443971222%

# f = open('simple_english.txt')
# raw = f.read()
# text = t.tokenize(raw)
# test_text(text)
# # Result: 98.74025194961008%

# # Test all Gutenberg Texts
# count = 0
# total = 0
# for fileid in gutenberg.fileids():
#     print(fileid)
#     count += test_text(gutenberg.words(fileid))
#     total += 1
# print(count / total)
# # result = 97.75693571924204%
# # lower than avg mostly due to less success with Shakespeare

print('\nEnter text to be converted to Pig Latin and back:')
while True:
    text = input()
    text = t.tokenize(text)
    pig = text_to_pig(text)

    print(' '.join(d.detokenize(pig)))
    print(' '.join(d.detokenize(pig_to_text(pig, freq, words, b_clust))))
    print()