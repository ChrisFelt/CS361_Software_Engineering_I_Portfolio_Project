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
            with open(name + '.json', 'r') as in_file:
                self._data = json.load(in_file)

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

    def save_cards(self):

        with open(self._name + '.json', 'w') as out_file:
            out_file.write(json.dumps(self._data))


class Card:
    pass


class Collection:
    pass


def authenticate(name, pwd):
    """checks user name/pwd against existing credentials"""
    # check if user credential txt file exists
    file = Path(name + ".txt")
    if file.is_file():
        # open and read file
        with open(name + '.txt', 'r') as in_file:
            credential = json.load(in_file)

        # check if pwd matches file contents
        if str(credential[name]) == pwd:
            return True

    return False


def print_divide():
    """prints a screen divide"""
    print("\n"
          "\n---------------------------------------------"
          "\n")


def login():
    """login screen routine"""

    print_divide()

    while True:

        user_input = input("\n1. Enter Username"
                           "\n2. Return to previous screen"
                           "\n-> ")

        # attempt login
        if user_input == "1":
            name = input("\n\nUsername -> ")
            pwd = input("\nPassword -> ")

            # authenticate input
            if authenticate(name, pwd) is True:
                # access account
                print("\n\nSuccess! Opening your account, " + name + ".")
                account(name, pwd)

            else:
                # retry
                print("\nLogin failed. Please enter a valid Username and password.\n")
                continue

            # if return from successful account login, exit login loop
            break

        else:
            # go back to main screen
            print_divide()
            return


def account(name, pwd):
    pass


if __name__ == '__main__':

    while True:

        user_input = input("Welcome to FlashCard! Please choose an option: "
                           "\n1. Login"
                           "\n2. Create new account"
                           "\n3. Help options"
                           "\n-> ")

        if user_input == "1":
            login()

        elif user_input == "2":
            pass

        else:
            pass
