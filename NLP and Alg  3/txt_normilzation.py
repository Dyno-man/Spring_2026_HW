"""
lowercasing, removing punctuation, tokenization, removing stop words, and stemming
"""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

doc1 = "She sells sea shells by the seashore."
doc2 = "How much wood would a woodchuck chuck, if a woodchuck could chuck wood?"
doc3 = "A journey of a thousand miles begins with a single step."

docs = [doc1, doc2, doc3]

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


# Normalize Docs
for doc in docs:
    tokenized_docs.append(normalize(doc))

# Find Vocab for docs
for doc in tokenized_docs:
    vocab_docs.append(vocab(doc))

num = 1 
for token in tokenized_docs:
    print(f"Amount of Tokens for doc {num}: ", end='')
    print(len(token))
    num +=1

print()

num = 1 
for token in vocab_docs:
    print(f"Amount of vocab for doc {num}: ", end='')
    print(len(token))
    num +=1
        
print(tokenized_docs)
print(vocab_docs)