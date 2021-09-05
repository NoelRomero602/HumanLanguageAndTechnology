#Noel Romero
#NXR170030
#CS 4395.001
#Dr. Mazidi
import re
import sys

import pickle

import pathlib  # used by method 2


## this class repesents the persons class for this hw 
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee id: %s \n %s %s %s \n %s" % (self.id, self.last, self.mi, self.first, self.phone))

    def get_id(self):
        return self.id

## this method reads the data file and begins to call the correct helper methods 
def processDataFile(filepath: str, persondict: dict):
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        text_in = f.read().splitlines()
        return process_lines(text_in[1:], persondict)

## this method will return a dict object containing the person objects 
def process_lines(text_in : str, persondict: dict):
    for element in text_in:
        person = verify_line(element, persondict)
        if persondict.get(person.get_id()):
            print("ID: %s is a duplicate " % person.get_id())
        else:
            persondict[person.get_id()] = person
    return persondict

## this method checks if the id is valid and if it's not a duplicate 
def verify_id(id: str, persondict: dict):
    pattern = re.compile('[a-zA-Z]{2}[0-9]{4}')
    loop_flag = True

    while loop_flag:
        matches = pattern.search(id)
        if matches:
            loop_flag = False
        else:
            print("ID invalid: %s \nID is two letters followed by 4 digits" % id)
            id = input("Please enter a valid id: ")

    return id

## this method checks if the phone number was entered correctly if not it will loop through until it is entered in the correct formatt
def verify_phone_number(phone: str):
    pattern = re.compile("[0-9]{3}\-[0-9]{3}\-[0-9]{4}")
    loop_flag = True

    while loop_flag:
        matches = pattern.search(phone)
        if matches:
            print("Match found: %s" % matches.group())
            loop_flag = False
        else:
            print("Phone %s is invalid \nEnter phone number in form 123-456-7890" % phone)
            phone = input("Enter phone number: ")
    return phone

## this method is responsible for verifiying the attributes of the person object
def verify_line(line: str, persondict: dict):
    tokens = line.split(',')
    last = tokens[0].capitalize()
    first = tokens[1].capitalize()
    mi = tokens[2].upper() if not (not tokens[2]) else 'X'
    id = verify_id(tokens[3], persondict)
    phone = verify_phone_number(tokens[4])
    person = Person(last, first, mi, id, phone)
    return person

## this method is used to print out the contents of dictionary
def print_persondict(dict_in: dict):
    print("Employee list:\n")
    for id in dict_in:
         print("\n")
         person = dict_in[id]
         person.display()

## this is the main method
def main():
    persondict = dict()
    dict_in = dict()
    if len(sys.argv) < 2:
        print('Please enter a files path as system arg')
    else:
        fp = sys.argv[1]
        persondict = processDataFile(fp, persondict)
        pickle.dump(persondict, open('dict.p', 'wb'))
        dict_in = pickle.load(open('dict.p', 'rb'))
        print_persondict(dict_in)

if __name__ == '__main__':
    main()
