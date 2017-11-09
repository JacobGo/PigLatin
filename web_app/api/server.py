from pyg_latin.depigify import depigify 
from pyg_latin.pigify import pigify
from pyg_latin.data.loader import words_dictionary, occ, frequencies

from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()

from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, reqparse

app = Flask(__name__)
api = Api(app)

class Pigify(Resource):
    def put(self):
        text = request.form['text']
        original = text
        text = t.tokenize(text)
        text = pigify(text)
        text = ' '.join(d.detokenize(text))
        res = { 'original': original,
                'pig_latin': text }
        return res

class Depigify(Resource):
    def put(self):
        text = request.form['text']
        original = text
        text = t.tokenize(text)
        text = depigify(text, frequencies, words_dictionary, occ)
        text = ' '.join(d.detokenize(text))
        res = { 'original': original,
                'english': text }
        return res
            
class TestAccuracy(Resource):
    def put(self):
        text = request.form['text']
        original = text
        text = t.tokenize(text)
        new_text = depigify(pigify(text), frequencies, words_dictionary, occ)
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
        accuracy = count/total
        wrong_count = len(wrong)
        wrong = dict(set(wrong))
        new_text = ' '.join(d.detokenize(new_text))
        res = { 'original': original,
                'result': new_text,
                'accuracy': accuracy,
                'wrong': wrong,
                'wrong_count': wrong_count}
        return res

api.add_resource(Pigify, '/pigify')
api.add_resource(Depigify, '/depigify')
api.add_resource(TestAccuracy, '/test')

if __name__ == '__main__':
    app.run(debug=True)