# Noel Romero
# NXR170030
# CS 4395.001
# Dr. Mazidi

import pathlib
import sys
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

import nltk


def processDataFile(fp: str):
    with open(pathlib.Path.cwd().joinpath(fp), 'r') as f:
        text_in = f.read()
        text_in = text_in.replace('\n', ' ')
        return text_in

def createDicOfCounts(dict_stems: dict):
    dict_to_return = dict()
    for w in dict_stems:
        if isinstance(dict_stems[w], list):
            dict_to_return[w] = len(dict_stems[w])
    print(dict_to_return)
    return dict_to_return

def preprocessRawText(raw_text: str):
    text = raw_text.lower()
    text = re.sub('\d+', '', text)
    text = text.replace('--', '')
    text = re.sub(r'[^\w\s]', ' ', text)
    return text


def main():
    if len(sys.argv) < 2:
        print('Please enter a files path as system arg')
    else:
        fp = sys.argv[1]
        raw_text = processDataFile(fp)
        text = preprocessRawText(raw_text)
        tokens = word_tokenize(text)
        tokens_unique = set(tokens)

        print(f'\nNumber of Tokens Step 3: {len(tokens)}')

        print(f'\nNumber of unique tokens from Step 4: {len(tokens_unique)} ')

        important_words = [t for t in tokens_unique if (t not in stopwords.words('english'))]

        print(f'\n All Important Words Step 5: {important_words}\n\ncount{len(important_words)}')
        ps = PorterStemmer()
        stemmed_words = [ps.stem(t) for t in important_words]
        tupples = list(zip(important_words, stemmed_words))

        dict_stems = dict()

        # create a dictionary where the key is the stem and the value is a list of words
        for stemmed_word in stemmed_words:
            stemmed_list = [i for i in important_words if i.startswith(stemmed_word)]
            dict_stems[stemmed_word] = stemmed_list

        print(f'\n\n Step 8 number of dict entries: {len(dict_stems)}')
        dict_stems_counts = createDicOfCounts(dict_stems)
        sorted_stems_list = sorted(dict_stems_counts.items(), key=lambda x: x[1], reverse=True)
        count = 0
        # print out the top 25 dictionary entries
        for i in sorted_stems_list:
            if(count > 24):
                print('end')
                break
            else:
                count = count +1
                print(f'\n\nkey:{i[0]}  list{dict_stems.get(i[0])}')

        tags = nltk.pos_tag(tokens)
        postags_dict = dict()
        levenshtein_distance(dict_stems)
# post tag the tokens  and create a dict with key being the pos and the value being count of words w/ pos
        for word, pos in tags:
            value = postags_dict.get(pos)
            if(value):
                value = 1 + value
                postags_dict[pos] = value
            else:
                value = 1
                postags_dict[pos] = value
        print(f'Step 12 postags_dict: \n\n{postags_dict}')


def levenshtein_distance(dict_stems: dict()):
    continu_list = dict_stems['continu']
    continue_str = 'continue'
    for w in continu_list:
        print(f'\nLevenshtein distance btw {w}: and continue is:{levenshtein(w,continue_str)}')

def levenshtein(a: str, b: str):
    if not a:
        return len(b)
    if not b:
        return len(a)
    return min(
        levenshtein(a[1:], b[1:]) + (a[0] != b[0]), # Case 1
        levenshtein(a[1:],b) + 1,
        levenshtein(a, b[1:]) +1
    )
if __name__ == '__main__':
    main()
