"""
lowercasing, removing punctuation, tokenization, removing stop words, and stemming
"""
import re
import string
import nltk
import copy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

text = "The day was grey and bitter cold, and the dogs would not take the scent. " \
"The big black hound had taken one sniff at the bear tracks, backed off, and skulked back to the pack with her tail between her legs."

def normalize(sentence):
    # Lowercase
    sentence = sentence.lower()

    # Remove punctuation
    punc = f'[{re.escape(string.punctuation)}]'
    sentence = re.sub(punc, "", sentence)
    
    # Tokenize
    tokens = sentence.split()

    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    tokens = [stemmer.stem(word) for word in tokens]
    return tokens


def vocab(sentence):
    seen = set()
    out = []
    for word in sentence:
        if word not in seen:
            seen.add(word)
            out.append(word)
    return out

tokenized_docs = []
vocab_docs = []


def punc_lower(text):
    text = text.lower()

    punc = f'[{re.escape(string.punctuation)}]'
    text = re.sub(punc, '', text)

    return text

processed_text = punc_lower(text)

def tokenize(text):
    return text.split()

tokenized_text = tokenize(processed_text)
vocabulary = vocab(tokenized_text)

def unigram(token):
    keys = {}

    for s in token:
        if s not in keys:
            keys.update({s : 1})
        else:
            temp = keys.get(s)
            temp += 1
            keys.update({s : temp})
    return keys

def unigram_probs(probs):
    total = 0

    for key in probs:
        total += probs.get(key)

    new_probs = copy.deepcopy(probs)

    for key in probs:
        val = probs.get(key)
        temp = val / total
        new_probs.update({key : temp})
    
    return new_probs

def lap_uni(probs):
    total = 0

    for key in probs:
        total += probs.get(key)

    new_probs = copy.deepcopy(probs)

    for key in probs:
        val = probs.get(key)
        temp = (val + 1) / (total + len(vocabulary))
        new_probs.update({key : temp})
    
    return new_probs

counts = unigram(tokenized_text)

print(counts)
print()
# Probabilities without smoothing
print(unigram_probs(counts))
print()
print(lap_uni(counts))


