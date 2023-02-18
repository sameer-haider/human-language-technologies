import sys
from random import seed
from random import randint
import nltk

# Check arg
if len(sys.argv) != 2:
    print("Error: no system arg present")
    sys.exit(1)

# Read file
file_name = sys.argv[1]
try:
    with open(file_name, 'r') as f:
        raw_text = f.read().lower()
except IOError:
    print("Error: Could not open file.")
    sys.exit(1)

# Tokenize and calc lexical diversity
tokens = nltk.word_tokenize(raw_text)
lex_div = len(set(tokens)) / len(tokens)
print("Lexical diversity:", lex_div)


# Preprocess func
def preprocess(raw_text):
    tokens = nltk.word_tokenize(raw_text)
    # Reduce to alpha, != stopwords, and len > 5
    tokens = [t for t in tokens if t.isalpha() and t not in nltk.corpus.stopwords.words('english') and len(t) > 5]
    # Lemmatize
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemmas = set([lemmatizer.lemmatize(t) for t in tokens])
    # POS tagging
    pos_tag = nltk.pos_tag(lemmas)
    print("First 20 tagged lemmas\n", pos_tag[:20])
    # Nouns
    nouns = [l for l in lemmas if nltk.corpus.wordnet.synsets(l, pos='n')]
    print("Number of tokens:", len(tokens))
    print("Number of nouns:", len(nouns))
    return tokens, nouns


# Make dictionary of nouns and their counts
tokens, nouns = preprocess(raw_text)
counts = {}
for n in nouns:
    counts[n] = tokens.count(n)

# Sort and save top 50
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
top_50 = [word for word, count in sorted_counts[:50]]
print("Top 50 common words:", top_50)


# Guessing game func
def guessing_game(top_50):
    score = 5
    while score > 0:
        # Randomly pick a word
        seed()
        word = top_50[randint(0, 49)]
        game = ['_' for w in word]
        print("Round start")
        print(' '.join(game))
        # Guess
        while score > 0:
            letter = input("Guess a letter:")
            if letter == '!':
                print("Game end")
                return
            elif letter in word:
                score += 1
                print("Right!", "Score is:", score)
                for i in range(len(word)):
                    if word[i] == letter:
                        game[i] = word[i]
                print(' '.join(game))
            else:
                score -= 1
                print("Sorry, guess again", "Score is:", score)
                print(' '.join(game))
            if game == list(word):
                print("You solved it!")
                print("Current score:", score)
                break

    print("Game end")
    return


# Call guessing game
guessing_game(top_50)
