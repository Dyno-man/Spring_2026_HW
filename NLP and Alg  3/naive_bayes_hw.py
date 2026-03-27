import math
import re
import string

training_data = [
    ("A", "i like chinese food"),
    ("A", "french food is her favorite"),
    ("A", "i enjoy food of all types"),
    ("B", "i like horror movies"),
    ("B", "do you enjoy funny movies")
]

test_doc = "i want food now ?"


def preprocess(text):
    text = text.lower()
    punc = f'[{re.escape(string.punctuation)}]'
    text = re.sub(punc, "", text)
    return text.split()


def process_docs(data):
    docs = []

    for label, text in data:
        docs.append((label, preprocess(text)))

    return docs


def get_vocab(docs):
    words = []

    for item in docs:
        label = item[0]
        tokens = item[1]

        for word in tokens:
            if word not in words:
                words.append(word)

    words.sort()
    return words


def get_priors(docs):
    counts = {}
    priors = {}
    total = len(docs)

    for item in docs:
        label = item[0]

        if label not in counts:
            counts[label] = 1
        else:
            counts[label] += 1

    for label in counts:
        priors[label] = counts[label] / total

    return priors


def get_word_counts(docs):
    class_words = {}
    class_totals = {}

    for item in docs:
        label = item[0]
        tokens = item[1]

        if label not in class_words:
            class_words[label] = {}
            class_totals[label] = 0

        for word in tokens:
            if word not in class_words[label]:
                class_words[label][word] = 1
            else:
                class_words[label][word] += 1

            class_totals[label] += 1

    return class_words, class_totals


def get_cond_probs(class_words, class_totals, vocab):
    cond_probs = {}
    vocab_size = len(vocab)

    for label in class_words:
        cond_probs[label] = {}
        denom = class_totals[label] + vocab_size

        for word in vocab:
            count = class_words[label].get(word, 0)
            cond_probs[label][word] = (count + 1) / denom

    return cond_probs


def get_test_counts(test_words, vocab):
    counts = {}
    ignored = []

    for word in test_words:
        if word in vocab:
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1
        else:
            ignored.append(word)

    return counts, ignored


def naive_bayes(priors, cond_probs, test_counts):
    scores = {}
    log_scores = {}

    for label in priors:
        score = priors[label]
        log_score = math.log(priors[label])

        for word in test_counts:
            count = test_counts[word]
            prob = cond_probs[label][word]

            score *= prob ** count
            log_score += count * math.log(prob)

        scores[label] = score
        log_scores[label] = log_score

    return scores, log_scores


processed_training = process_docs(training_data)
processed_test = preprocess(test_doc)
vocabulary = get_vocab(processed_training)

priors = get_priors(processed_training)
class_words, class_totals = get_word_counts(processed_training)
cond_probs = get_cond_probs(class_words, class_totals, vocabulary)
test_counts, ignored_words = get_test_counts(processed_test, vocabulary)
scores, log_scores = naive_bayes(priors, cond_probs, test_counts)

prediction = max(scores, key=scores.get)

print("training docs")
print(processed_training)
print()

print("test doc")
print(processed_test)
print()

print("vocabulary")
print(vocabulary)
print("|V| =", len(vocabulary))
print()

print("priors")
print(priors)
print()

print("word counts")
print(class_words)
print()

print("token totals")
print(class_totals)
print()

print("test counts")
print(test_counts)
print()

print("ignored words")
print(ignored_words)
print()

print("scores")
print(scores)
print()

print("log scores")
print(log_scores)
print()

print("prediction")
print(prediction)
