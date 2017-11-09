vowels = 'aeiou'

# We use a lemmatizer for a small accuracy boost
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Re for onset consonant cluster detection
import re

'''
Algorithm

0) Strip capitilization and save for later
1) Slice off '-ay'
2) Generate all possible permutations by moving consonants to front from right until hitting a vowel
3) For each permutation check if it (or its lemma) is in the word database
    3a) If it is, add it to a list
3) If the list is empty, add the permutation with the most common consonant cluster onset to the list
4) If the list is still empty, resort to permutations themselves
5) Choose the result from the list with the highest frequency based on our word database (built from brown, reuters, nltk.words, and stopwords)
6) In a tie, choose the most common consonant cluster onset
7) Add back capitlization and return result

'''

def english_speak(word):
    # if single letter or punctuation/numeric, return it (e2p shouldn't add -ay)
    if len(word) < 1 or not word.isalpha():
        return word

    # Handle capitization.
    # create a list of booleans corresponding to the presence of capitals in word
    # 'WoRd' -> 'True,False,True,False'
    cap = []
    for i in range(0,len(word) - 2):
        if word[i].isupper():
            cap.append(True)
        else:
            cap.append(False)

    # Here we iterate through the word and create a list of permutations of consonant clusters.
    word = word.lower()[:-2]    # lower case + strip -ay
    cluster = ''                # consonant cluster which grows as we iterate through the word
    permutations = []           # all permutations of consonant clusters (ex: ayspr -> [ayspr, raysp, prays, spray])
    index = len(word) - 1       # index in word starting at end
    permutations.append(word)   # add the pig latin word for words like aay -> a
    for i,c in enumerate(reversed(word)):   # iterate through reversed word where i is count and c is current character
        i = len(word) - 1 - i               # adjust i to be from end instead of start
        if c == 'u' and word[i-1] == 'q':   # handle 'qu'
            cluster = 'qu' + cluster        # prepend to cluster
            new_word = cluster + word[:index - 1]   # put cluster at the beginning, adjust for 'qu' pair
            index -= 1  # decrement index
        elif c == 'q':  # adjust for q as well
            index -= 1
            new_word = cluster + word[:index + 1]
        elif c in vowels:   # stop iterating once we hit a vowel
            break
        else:   # add to cluster and form a new word starting with cluster
            cluster = c + cluster
            new_word = cluster + word[:index]
            index -= 1
        permutations.append(new_word)

    # We iterate through our permutations and build a list of all words actually within our corpus.
    result = []

    t = word
    for word in permutations:   # if the lemma of the permutation or the permutation itself is within our set of words, add it the results; 
        if lemmatizer.lemmatize(word) in words or word in words: # using lemmas boosts accuracy a tiny bit
            result.append(word)
    
    if len(result) == 0: # if none of the permutations are words we choose the one with the most likely onset
        for word in permutations:
            onset = re.findall('^[bcdfghjklmnpqrstvwxz]{1,}', word)
            if onset:
                onset = onset[0]
                if onset in bc:
                    result.append((word, bc[onset]))                
        if result:
            result = [ max(result, key=lambda f:f[1])[0] ]

    if len(result) == 0:
        # if none of permutations are words or have a valid consonant cluster onset, continue with the permutations themselves
        result = permutations

    # We make a list of pairs with the possible words and their frequencies, then choose the one with the highest frequency, giving ~10-15% improved results
    freqs = []
    for word in result:
        pair = [word, 0]
        if word in freq:
            pair[1] = freq[word]
        freqs.append(pair)
    freqs = sorted(freqs, key=lambda x: x[1])
    freqs.reverse()
    temp = freqs[0][0] if len(freqs) > 0 else result[0]

    # if we have a tie, choose the one with the most likely onset (Mostly just fixes some strange behavior with freq[tub] == freq[btu])
    if len(freqs) >= 2 and freqs[0][1] == freqs[1][1]:
        possible = []
        for pair in freqs[:2]:
            word = pair[0]
            onset = re.findall('^[bcdfghjklmnpqrstvwxz]{1,}', word)
            if onset:
                onset = onset[0]
                if onset in bc:
                    possible.append((word, bc[onset]))
        if len(possible) > 0:
            possible = sorted(possible, key = lambda x: x[1])
            possible.reverse()
            temp = possible[0][0]

    # Add capitilization back in using our list of booleans
    res = ''
    for i in range(0,len(temp)):
        if cap[i]:
            res += (temp[i].upper())
        else:
            res += (temp[i])
    return res

def pig_to_text(text, _freq, _words, _bc):
    # We instantiate our imported frequencies, word list, and onset consonant clusters
    global freq, words, bc
    freq = _freq
    words = _words
    bc = _bc
    return [english_speak(word) for word in text]