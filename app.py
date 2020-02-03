#Text Extractor Service By Ganesh Ghag
import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def extract_dates(in1):
    r1 = re.compile(r'\d{4}[- /.]\d{2}[- /.]\d{2}')
    r2 = re.compile(r'\d{2}[- /.]\d{2}[- /.]\d{4}')
    return r1.findall(in1) + r2.findall(in1)

def extract_DecimalAmounts(in1):
    r = re.compile(r'[0-9]\d*,?\d*,?\d*,?\d*.?\d*')  
    return r.findall(in1)


def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

def extract_all(input):
    return [extract_email_addresses(input), extract_phone_numbers(input),extract_dates(input),extract_DecimalAmounts(input), extract_names(input)]

#Web app Flask related code starts here >>>>>>>>>>>>>>>>>>>>>>>
import json
from flask import jsonify
from flask import Flask
from flask import request

app = Flask(__name__)

#Sample CURL command as input: curl -X POST --data-binary "@sampletext1.txt" http://127.0.0.1:5000/
@app.route('/',methods = ['POST'])
def index():
	s = extract_all(request.get_data(as_text=True))
	return jsonify(s)

if __name__ == '__main__':
	app.run(debug=True)
