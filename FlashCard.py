# Title: Flash Card App
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: A flash card app that runs via a command prompt interface.

import json
from pathlib import Path


class User:

    # initialize data members
    def __init__(self, name, pwd):

        # open and read user's json file if it exists
        data_file = Path(name + ".json")
        if data_file.is_file():
            # open file and load into data
            with open(name + '.json', 'r') as infile:
                self._data = json.load(infile)[0]

        # dictionary defaults to None
        else:
            self._data = None

        # save user details
        self._name = name
        self._pwd = pwd
        self._cred = {name: pwd}

        # check if credential file exists
        cred_file = Path(name + ".txt")
        if cred_file.is_file() is False:
            # create credentials file if it did not exist
            with open(name + ".txt", 'w') as file:
                file.write(json.dumps(self._cred))

    def add_card(self, front, back):
        # create dictionary if no cards
        if self._data is None:
            self._data = {front: back}

        # add card to dictionary
        else:
            self._data[front] = back

    def print_front(self):
        # print front nad back of card in order sorted by front
        for front, back in sorted(self._data.items()):
            print(front)
            input("Press any key to continue...")
            print(back)


class Card:
    pass


class Collection:
    pass


def login(name, pwd):

    # check if user credential txt file exists
    file = Path(name + ".txt")
    if file.is_file():
        # read file
        read_line = file.readline()
        file.close()
        # check if pwd matches file contents
        if read_line == pwd:
            return True

    return False


if __name__ == '__main__':
    pass
