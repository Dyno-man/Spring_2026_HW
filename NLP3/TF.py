import math

doc1 = "it is going to rain today"
doc2 = "today i am not going outside"
doc3 = "NLP is an interesting topic"

all_docs = [doc1, doc2, doc3]
DOC_COUNT = len(all_docs)

docs = doc1.split() + doc2.split() + doc3.split()

def vocab(doc):
    unique_words = []
    for word in doc:
        if word not in unique_words:
            unique_words.append(word)
    return unique_words

def tf(vocab, doc):
    voc_freq = [0] * len(vocab)
    doc = doc.split()
    for x in range(len(vocab)):
        c = 0
        for y in doc:
            if vocab[x] == y:
                c += 1
        voc_freq[x] = c / len(doc)
    return voc_freq

def idf(vocab, all_docs):
    word_freq = []
    for word in vocab:
        doc_freq = 0
        for doc in all_docs:
            if word in doc.split():
                doc_freq += 1
        word_freq.append(math.log(DOC_COUNT / doc_freq))
    return word_freq

vo = vocab(docs)

f_doc1 = tf(vo, doc1)
f_doc2 = tf(vo, doc2)
f_doc3 = tf(vo, doc3)

freq_docs = [f_doc1, f_doc2, f_doc3]

print(vo)
print(freq_docs)
print(idf(vo, all_docs))