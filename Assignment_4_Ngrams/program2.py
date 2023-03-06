# Created By: Priyesh Patel (Php180002) and Sameer Haider (sah190005)
# Used Pickled Bigram and Unigram Dictionaries to calcuated language probablity

import pickle
from nltk import word_tokenize, ngrams

def calculate_prob(text, bigram_dict, unigram_dict, V):
    #algorithm from Github
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    prob = 1

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        prob = prob * ((n + 1) / (d + V))
    return prob

def write_prob_to_file(file, line, english_prob, french_prob, italian_prob):
    f = open(file, 'a')
    if english_prob > french_prob and english_prob > italian_prob:
        f.write('%d English\n' % line)
    elif french_prob > english_prob and french_prob > italian_prob:
        f.write('%d French\n' % line)
    else:
        f.write('%d Italian\n' % line)
    f.close()

def compare_files(file1, file2):
    file1 = open(file1, 'r')
    file2 = open(file2, 'r')

    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

    total = 0
    correct = 0
    for line1, line2 in zip(file1_lines, file2_lines):
        if line1 == line2:
            correct += 1
        # check which line are different
        #else:
        #    print(line1 + line2)
        total += 1
    file1.close()
    file2.close()

    return correct / total * 100

if __name__ == "__main__":

    #load bigram data from pickled files
    english_bigrams_dict = pickle.load(open('pickles/english_bigrams.pkl', 'rb'))
    french_bigrams_dict = pickle.load(open('pickles/french_bigrams.pkl', 'rb'))
    italian_bigrams_dict = pickle.load(open('pickles/italian_bigrams.pkl', 'rb'))

    #load unigram data from pickled files
    english_unigrams_dict = pickle.load(open('pickles/english_unigrams.pkl', 'rb'))
    french_unigrams_dict = pickle.load(open('pickles/french_unigrams.pkl', 'rb'))
    italian_unigrams_dict = pickle.load(open('pickles/italian_unigrams.pkl', 'rb'))

    V = len(english_unigrams_dict) + len(french_unigrams_dict) + len(french_unigrams_dict)

    #clear output file
    with open("data/LangId.output", 'r+') as file:
        file.truncate(0)

    test_file = open('data/LangId.test', 'r')
    line_count = 1

    #iterate throught test file as guess probability
    for line in test_file.readlines():
        english_prob = calculate_prob(line, english_bigrams_dict, english_unigrams_dict, V)
        french_prob = calculate_prob(line, french_bigrams_dict, french_unigrams_dict, V)
        italian_prob = calculate_prob(line, italian_bigrams_dict, italian_unigrams_dict, V)
        write_prob_to_file('data/LangId.output', line_count, english_prob, french_prob, italian_prob)
        line_count += 1

    print('Accuracy from output and solutions is %.2f' % compare_files('data/LangId.output','data/LangId.sol'))

