# Noel Romero
# NXR170030
# CS 4395.001
# Dr. Mazidi

import pathlib
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

def processDataFile(filepath: str):
    with open(pathlib.Path.cwd().joinpath(filepath),'r') as f:
        text_in = f.read()
        text_in = text_in.replace('\n', ' ')
        return text_in

def preProcessRawText(raw_text):
    tokens = word_tokenize(raw_text)
    # Part 3A lowercase, get rid of punctuation, numbers, stop words and words with lengths less than 5
    tokens = [t.lower() for t in tokens if (t.isalpha() and (len(t) > 5) and (t not in stopwords.words('english')))]
    tokens_unique = set(tokens)
    print("\nLexical diversity: %.2f" % (len(tokens_unique) / len(tokens)))
    text_const = Text(tokens)
    wnl = WordNetLemmatizer()

    # Part 3B make a list of unique lemmas
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))
    # Part 3C do pos tagging of the unique lemmas and print the 1st 20
    tags = nltk.pos_tag(lemmas_unique)
    print("First 20 tagged items:\n", tags[:19])
    # Part 3d get all the nouns
    lemmas_nouns = [word for word, pos in tags\
                    if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    # Part 3e
    print('The number of tokens is:\n', len(tokens))
    print('The number of nouns is:\n', len(lemmas_nouns))
    return tokens, lemmas_nouns

def guessing_game_parent(common_words:list):
    game_on = True
    score = 5
    word_match = False
    seed(1234)
    while game_on:

        random_index = randint(1,49)
        chosen_word = common_words[random_index]
        word_match, score = guessing_game(chosen_word, score)
        if(word_match):
            print("You solved it!\nCurrent score:", score)
        else:
            print(f"Game over the correct word was: {chosen_word} and the score was: {score}")
            game_on = False

def guessing_game(chosen_word:str, score:int):
    game_on = True
    word_match = True
    guesses = []

    while game_on:
        for letter in chosen_word:
            if letter.lower() in guesses:
                print(letter, end=" ")
            else:
                print("_", end=" ")
        print("")


        guess = input("Guess a letter:")
        guesses.append(guess.lower())
        if guess.lower() not in chosen_word.lower():
            score -=1
            if guess == '!':
                word_match = False
                break
            print("Sorry, guess again. Score is ", score)
            if score <= 0:
                break
        else:
            score +=1
            print("Right! Score is ", score)

        game_on = True
        word_match = True
        for letter in chosen_word:
            if letter.lower() not in guesses:
                word_match = False
                break
        if(word_match):
            game_on = False
    return word_match,score




def main():
    if len(sys.argv) < 2:
        print('Please enter a files path as system arg')
    else:
        fp = sys.argv[1]
        raw_text = processDataFile(fp)
        tokens, lemmas_nouns = preProcessRawText(raw_text)
        # make a dictionary of counts
        nlk_tokens = Text(tokens)
        count_dict = {t:nlk_tokens.count(t) for t in lemmas_nouns}
        sorted_counts_list = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        print("The 50 most common words are:\n")
        for i in range(50):
            print(sorted_counts_list[i])
        fifty_most_common_wordslist = [word for word, count in sorted_counts_list[:50]]
        print("List of 50:\n", fifty_most_common_wordslist)
        guessing_game_parent(fifty_most_common_wordslist)

if __name__ == '__main__':
    main()
