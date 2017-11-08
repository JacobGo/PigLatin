import re
from string import punctuation
def pig_speak(word):
	# empty string returns empty string
	if word=='':
		return ''

	# just punctuation mark returns punctuation mark
	if word in punctuation or not word.isalpha():
		return word

	regex = '[AEIOUaeiou]' # any vowels in any order
	
	cap = []
	for i in range(0, len(word)):
		if word[i].isupper():
			cap.append(True)
		else:
			cap.append(False)
	
	# find the index of the first vowel (if all consonants then re.search is None (false) so index = 0)
	start = re.search(regex, word).start() if re.search(regex, word) else 0

	# adjust for (consonant)*qu like quiet and squirrel
	if word[0] not in 'aeiou' and (word[1:3].lower() == 'qu' or word[:2].lower() == 'qu'):
		start = 3 if word[1:3].lower() == 'qu' else 2

	# we substitute out punctuation from a string where we move the letters before the first
	# vowel (our consonant cluster) and then add ay and make lower case
	result = re.sub('[^\w\s]', '', (word[start:] + word[:start] + 'ay').lower());

	# if input is capitalized, add back captilization
	temp = result[0:len(result) - 2]
	result = ''
	for i in range(0,len(temp)):
		if cap[i]:
			result += (temp[i].upper())
		else:
			result += (temp[i])
	result = result + 'ay'
	# if input ends with punctuation, append it
	if not word[-1].isalpha():
		result+=word[-1]

	return result

def text_to_pig(text):
	# apply pig_speak to each word in text
	return [pig_speak(word) for word in text]

# # converts input to pig latin 
# while True:
# 	print(' '.join(text_to_pig(input().split(' '))))