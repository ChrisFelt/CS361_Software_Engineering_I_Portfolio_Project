# Title: Flash Card App
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: A flash card app that runs via a command prompt interface.

import json
from pathlib import Path
import os


class User:
    """Represents a user, with credentials and flash cards."""
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
        """adds a flash card entry to user._data"""
        # create dictionary if no cards
        if self._data is None:
            self._data = {front: back}

        # add card to dictionary
        else:
            self._data[front] = back

    def print_front(self):
        """prints flash cards in self._data starting from with the front"""
        # print front nad back of card in order sorted by front
        for front, back in sorted(self._data.items()):
            print("\nFront: " + front)
            input("Press any key to continue...")
            print("Back: " + back)
            input("Press any key to continue...")

    def save_cards(self):
        """saves self.data contents as a json to same directory"""
        with open(self._name + '.json', 'w') as out_file:
            out_file.write(json.dumps(self._data))

    def delete(self):
        """deletes cards from self._data and from hard drive"""
        # delete data
        self._data = {}
        # delete file if it exists
        data_file = Path(self._name + ".json")
        if data_file.is_file():
            os.remove(self._name + '.json')

    def no_cards(self):
        """returns true if user has no cards, otherwise false"""
        if self._data == {}:
            return True
        else:
            return False


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
        # prompt user
        login_input = input("\n1. Enter Username"
                            "\n2. Return to previous screen"
                            "\n-> ")

        # attempt login
        if login_input == "1":
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
    """account screen routine"""

    # create user object with credentials
    user = User(name, pwd)

    while True:
        print_divide()
        # prompt user
        account_input = input("Welcome to your account! Please enter the number of the option you wish below."
                              "\n1. View your flash cards"
                              "\n2. Create new flash card - customizable in just two steps!"
                              "\n3. Edit/delete your flash cards"
                              "\n4. Logoff"
                              "\n5. Help options"
                              "\n-> ")

        # display flash card
        if account_input == "1":

            if user.no_cards():
                print("\nYou currently have no cards to view! Please make a new card from your account menu.")

            else:
                user.print_front()

        # create flash card
        elif account_input == "2":
            # prompt user for front and back
            front = input("Please enter text for front of card: ")
            back = input("Please enter text for back of card: ")

            # confirm card
            print("\nYou have entered front: " + front + "\n And back: " + back)
            finalize = input("\nSave this card? Y/N: ")

            # save card
            if finalize.lower() == "y":
                print("Card saved!")
                user.add_card(front, back)

            # do nothing
            elif finalize.lower() == "n":
                print("Card not saved.")
                continue

            else:
                print("Invalid entry. Returning to account.")

        # delete ALL cards
        elif account_input == "3":
            # confirm choice to delete
            delete = input("Delete your card(s)? Y/N: ")

            # delete all cards in user object and hdd flash card file associated with user credentials
            if delete.lower() == "y":
                print("Cards deleted!")
                user.delete()

            # do nothing
            elif delete.lower() == "n":
                print("Cards will not be deleted.")
                continue

            else:
                print("Invalid entry. Returning to account.")

        # logoff user
        elif account_input == "4":
            # first save data to hdd
            user.save_cards()
            # return to previous menu
            break

        else:
            print("Welcome to user account help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to your account menu, press any key...")
            continue


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
