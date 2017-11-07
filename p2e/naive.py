vowels = 'aeiou'
from nltk.stem import WordNetLemmatizer
from string import punctuation
lemmatizer = WordNetLemmatizer()

def english_speak(word):
    if len(word) < 1 or word in punctuation:
        return word
    cap = word[0].isupper()
    word = word.lower()[:-2]
    cluster = ''
    permutations = []
    index = len(word) - 1
    permutations.append(word)
    for i,c in enumerate(reversed(word)):
        print(word[-i-1])
        if c == 'u' and word[-i-1] == 'q':
            cluster = 'qu' + cluster
            new_word = cluster + word[:index]
            print(new_word)
            index -= 2
        elif c in vowels:
            break
        else:
            cluster = c + cluster
            new_word = cluster + word[:index]
            index -= 1
        permutations.append(new_word)

    result = []
    for word in permutations:
        if lemmatizer.lemmatize(word) in words:
            result.append(word)
    if len(result) == 0:
        result = permutations
    freqs = (sorted([(word, freq[lemmatizer.lemmatize(word)]) for word in result], key=lambda x: x[1]))
    freqs.reverse()
    return (freqs[0][0][0].upper() + freqs[0][0][1:]) if cap else freqs[0][0]

def pig_to_text(text, _freq, _words):
    global freq
    global words
    freq = _freq
    words = _words
    return [english_speak(word) for word in text]