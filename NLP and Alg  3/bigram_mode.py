import re, string
from collections import Counter, defaultdict

text = """The day was grey and bitter cold, and the dogs would not take the scent.
The big black hound had taken one sniff at the bear tracks, backed off,
and skulked back to the pack with her tail between her legs."""

# ----------------------------
# 1. Preprocessing
# ----------------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    return text

processed = preprocess(text)
tokens = processed.split()

print("Preprocessed Text:\n")
print(processed)
print("\nTotal Tokens:", len(tokens))

# ----------------------------
# 2. Vocabulary
# ----------------------------
vocab = sorted(set(tokens))
V = len(vocab)

print("Vocabulary Size |V| =", V)
print()

# ----------------------------
# 3. Bigram Raw Counts
# ----------------------------
bigram_counts = Counter(zip(tokens[:-1], tokens[1:]))
unigram_counts = Counter(tokens)

print("BIGRAM RAW COUNTS (Observed Only):\n")

for (w1, w2), c in bigram_counts.items():
    print(f"{w1:10} -> {w2:10} : {c}")

print()

# ----------------------------
# 4. Laplace Smoothed Counts
# ----------------------------
print("Laplace Smoothing Applied:")
print("Smoothed Count = Raw Count + 1")
print("Denominator = count(w1) + |V|\n")

# Example for one word (clean presentation)
example_word = "the"

print(f"Example Bigram Probabilities for previous word = '{example_word}':\n")

denom = unigram_counts[example_word] + V

for w2 in vocab:
    raw = bigram_counts[(example_word, w2)]
    smooth_count = raw + 1
    prob = smooth_count / denom
    print(f"{example_word:5} -> {w2:10} | Raw: {raw:2} | Smoothed: {smooth_count:2} | Prob: {prob:.4f}")

print()

# ----------------------------
# 5. Final Smoothed Probability Table (Observed Only)
# ----------------------------
print("Final Smoothed Probabilities (Observed Bigrams Only):\n")

for (w1, w2), raw in bigram_counts.items():
    prob = (raw + 1) / (unigram_counts[w1] + V)
    print(f"P({w2} | {w1}) = {prob:.4f}")