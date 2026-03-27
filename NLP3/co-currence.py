import math

doc1 = "it is going to rain today"
doc2 = "today i am not going outside"
doc3 = "NLP is an interesting topic"

all_docs = [doc1, doc2, doc3]

docs = doc1.split() + doc2.split() + doc3.split()

def vocab(doc):
    unique_words = []
    for word in doc:
        if word not in unique_words:
            unique_words.append(word)
    return unique_words

def co_matrix(vocab, all_docs, window):
    matrix = []
    
    for x in range(len(vocab)):
        row = [0] * len(vocab)
        matrix.append(row)
    
    for doc in all_docs:
        words = doc.split()
        
        for x in range(len(words)):
            center_word = words[x]
            center_index = vocab.index(center_word)
            
            start = x - window
            end = x + window
            
            if start < 0:
                start = 0
            if end >= len(words):
                end = len(words) - 1
            
            for y in range(start, end + 1):
                if x != y:
                    context_word = words[y]
                    context_index = vocab.index(context_word)
                    matrix[center_index][context_index] += 1
    
    return matrix



def cosine_sim(vec1, vec2):
    dot = 0
    mag1 = 0
    mag2 = 0
    
    for i in range(len(vec1)):
        dot += vec1[i] * vec2[i]
        mag1 += vec1[i] ** 2
        mag2 += vec2[i] ** 2
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    return dot / (math.sqrt(mag1) * math.sqrt(mag2))

def most_similar(vocab, matrix):
    best_score = -1
    best_pair = ("", "")
    
    for i in range(len(vocab)):
        for j in range(len(vocab)):
            if i != j:
                score = cosine_sim(matrix[i], matrix[j])
                
                if score > best_score:
                    best_score = score
                    best_pair = (vocab[i], vocab[j])
    
    return best_pair, best_score


vo = vocab(docs)

matrix = co_matrix(vo, all_docs, 2)

print("Vocabulary:")
print(vo)
print()

print("Co-occurrence Matrix:")
for row in matrix:
    print(row)


pair, score = most_similar(vo, matrix)

print("Most similar words:")
print(pair)
print("Cosine similarity:", score)