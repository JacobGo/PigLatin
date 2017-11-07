from e2p.assignment8_jacob_goldman import text_to_pig
from p2e.naive import pig_to_text
from nltk.corpus import words,reuters,brown,gutenberg
from nltk.probability import FreqDist
from string import punctuation

import re

print('Loading freqdist...')
freq = FreqDist(reuters.words())
words = set(reuters.words())


text = 'Squirrels query quarries spring string'.split()
print(pig_to_text(text_to_pig(text), freq, words))

# print('Pigify and depigify...')
# from nltk.corpus import gutenberg
# text = gutenberg.words('melville-moby_dick.txt')
# new_text = (pig_to_text(text_to_pig(text), freq, words))
# count = 0
# total = 0
# for i in range(0, len(text)):
#     if text[i] not in punctuation:
#         total += 1
#         if text[i] == new_text[i]:
#             count += 1
# print("Accuracy:", count / total)

# while True:
#     text = input()
#     text = re.sub('[^\w\s]', '', text).split(' ')
#     pig = text_to_pig(text)
#     print(' '.join(pig))
#     print(' '.join(pig_to_text(pig, freq, words)))