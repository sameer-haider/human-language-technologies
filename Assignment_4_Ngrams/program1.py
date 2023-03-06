import nltk
from nltk.util import ngrams
import pickle

def preprocess(filename, lang):
    # remove newlines
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', ' ')
    # tokenize
    tokens = nltk.word_tokenize(text, lang)
    unigrams = list(ngrams(tokens, 1))
    bigrams = list(ngrams(tokens, 2))
    # count dicts
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict


english_unigrams, english_bigrams = preprocess("data/LangId.train.English", 'english')
french_unigrams, french_bigrams = preprocess("data/LangId.train.French", 'french')
italian_unigrams, italian_bigrams = preprocess("data/LangId.train.Italian", 'italian')

with open('pickles/english_unigrams.pkl', 'wb') as f:
    pickle.dump(english_unigrams, f)
with open('pickles/english_bigrams.pkl', 'wb') as f:
    pickle.dump(english_bigrams, f)

with open('pickles/french_unigrams.pkl', 'wb') as f:
    pickle.dump(french_unigrams, f)
with open('pickles/french_bigrams.pkl', 'wb') as f:
    pickle.dump(french_bigrams, f)

with open('pickles/spanish_unigrams.pkl', 'wb') as f:
    pickle.dump(italian_unigrams, f)
with open('pickles/spanish_bigrams.pkl', 'wb') as f:
    pickle.dump(italian_bigrams, f)
