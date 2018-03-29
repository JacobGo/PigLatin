# pyglatin

Pyglatin is a Python script capable of translating English text into [Pig Latin](https://en.wikipedia.org/wiki/Pig_Latin), in which all consonants until the first vowel are moved to the end of the word and 'ay' is added. It can also translate back to English, which is not trivial when you encounter different potential permutations of consonants at the beginning/end of the word. We solve this using a frequency distribution to pick the most likely permutation, with some light rule-based phonetic filtering.
