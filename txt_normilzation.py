"""
lowercasing, removing punctuation, tokenization, removing stop words, and stemming
"""
import re
import string
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')


stop_words = set(stopwords.words('english'))


doc1 = "She sells sea shells by the seashore."
doc2 = "How much wood would a woodchuck chuck, if a woodchuck could chuck wood?"
doc3 = "A journey of a thousand miles begins with a single step."

docs = [doc1, doc2, doc3]

def normalize(sentence):
    #Lowering sentences
    sentence = sentence.lower()

    #Define all punctuation
    punc = f'[{re.escape(string.punctuation)}]'

    #Remove all punctuation
    sentence = re.sub(punc, "", sentence)

    sentence = [word for word in sentence if word not in stop_words]

    #Tokenize the sentence
    # sentence = sentence.split()

    return sentence


for stuff in docs:
    print(normalize(stuff))
