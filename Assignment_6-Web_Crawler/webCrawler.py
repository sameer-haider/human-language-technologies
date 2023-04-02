import os
import re
import string
import nltk
import requests
import sqlite3
from bs4 import BeautifulSoup

stopwords = nltk.corpus.stopwords.words('english')

#Web Crawler function take a starting url and finds related url to the topic of Intersellar
#return a list of possible urls (excluding, wiki, and times related urls)
def web_crawler(start_url):
    page = requests.get(start_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url_list = []

    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if link_str.startswith('http') and 'archive' not in link_str and '.org' not in link_str and 'times' not in link_str:
            if 'interstellar' in link_str or 'Interstaller' in link_str:
                url_list.append(link_str)
    return url_list

def web_scrape(url_list):

    counter = 1
    #for each url website scrape its paragraph content and write it to a file
    for url in url_list:
        with open('data/original_data%d' % counter, 'w') as f:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            for p in soup.select('p'):
                f.write(p.get_text() + '\n')
        counter +=1

def clean_file(directory):
    all_data = ""
    for filename in os.scandir(directory):
       if filename.is_file():
            #read files from data folder
            file = open(filename, 'r')
            new_filename = filename.path.replace('original', 'clean')
            data = file.read()
            #clean up data
            data = data.replace('\t','').replace('\n',' ')
            #use nltk to get sentence tokens
            sentences = nltk.sent_tokenize(data)
            all_data += data + " "
            with open(new_filename, 'w') as f:
                for sentence in sentences:
                    f.write(sentence + '\n')
    return all_data

def term_frequency(data):
    # Lowercase and remove punctuation
    data = data.lower()
    data = re.sub('[%s]' % re.escape(string.punctuation), '', data)
    # Tokenize
    tokens = nltk.word_tokenize(data)
    vocab = set()  # set of words

    # taken from kjmazidi/NLP
    tf_dict = {}
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords]

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    sorted_tf = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(40):
        print(f"{i+1}.", sorted_tf[i][0])

def knowledge_base(terms):
    # Create a new database file
    conn = sqlite3.connect('interstellar.db')
    d = conn.cursor()

    # Create table for each term, storing fact and id primary key
    for term in terms:
        table_name = term + "_facts"
        d.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, fact TEXT)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    starter_url = "https://en.wikipedia.org/wiki/Interstellar_(film)"
    all_urls = web_crawler(starter_url)

    with open('preferred_url.txt', 'r') as f:
        preferred_urls = [line.strip() for line in f]

    print('Chosen URLs:')
    print(*preferred_urls, sep='\n')

    web_scrape(preferred_urls)
    data = clean_file('data')
    term_frequency(data)
    top_10 = ['film', 'interstellar', 'hole',
              'science', 'time', 'nolan', 'years',
              'space', 'light', 'world']
    knowledge_base(top_10)





