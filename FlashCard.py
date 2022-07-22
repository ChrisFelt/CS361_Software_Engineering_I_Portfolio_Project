# Title: Flash Card App
# Class: CS 361 - Software Engineering I
# Author: Christopher Felt
# Description: A flash card app that runs via a command prompt interface.

import json
from pathlib import Path
import os
import zmq


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
            self._data = {}

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

    def add_card(self, pos, front, back):
        """adds a flash card entry to given collection in user._data"""
        pos = int(pos) - 1

        # create dictionary if no cards
        if self._data == {}:
            self._data = {list(self._data.keys())[pos]: {front: back}}

        # add card to dictionary
        else:
            self._data[list(self._data.keys())[pos]][front] = back

    def add_coll(self, coll):
        # adds an empty collection to self._data
        self._data[coll] = {}

    def show_coll(self):
        """prints a numbered list of all collections"""

        i = 1
        # print list
        for front, back in sorted(self._data.items()):
            print(str(i) + ". " + front)

            # screen break every 10 cards
            if i % 10 == 0:
                input("\nPress any key to continue...\n")

            i += 1

    def valid_index(self, pos):
        """check if the given index falls within the dictionary"""
        pos = int(pos) - 1
        if 0 <= pos < len(self._data):
            return True
        else:
            return False

    def show_cards(self):
        """given the index of a collection, prints a numbered list of all flash cards"""

        # print collection
        for j in range(len(self._data)):
            print(str(j + 1) + ". " + list(self._data.keys())[j])
            i = 1
            # print list
            # list(dict_name.keys())[0] gets key at position 0
            for front, back in sorted(self._data[list(self._data.keys())[j]].items()):
                print("    " + front)

                # screen break every 10 cards
                if i % 10 == 0:
                    input("\nPress any key to continue...\n")

                i += 1

    def print_front(self, pos):
        """given the index of a collection, prints flash cards in self._data in front -> back order"""
        pos = int(pos) - 1
        # print front and back of card in order sorted by front
        i = 1
        for front, back in sorted(self._data[list(self._data.keys())[pos]].items()):
            print("\nShowing flash card #" + str(i) + ".")
            print("Front: " + front)
            input("----------------")
            print("Back: " + back)
            input("Press any key to see next card...")

            i += 1

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

    def search(self, term):
        """search self._data for cards that match term"""
        context = zmq.Context()

        # connect to server with socket
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:7077")

        # send flash card JSON to search microservice
        socket.send_json(self._data)

        # get microservice response
        response = socket.recv_json()

        # check if search was successful
        if response["status"] != "done":
            print("\nSearch failed. Please try again.")

        else:
            # get search results from response
            result = response["data"]

            # if no match found, notify user
            if result == {}:
                print("\nNo matches found for " + term + ".")

            else:
                print("\nFound the following matches: ")
                i = 1
                # print list
                for front, back in sorted(self._data.items()):
                    print(str(i) + ". " + front + "  ||  " + back)

                    # screen break every 10 cards
                    if i % 10 == 0:
                        input("\nPress any key to continue...\n")

                    i += 1


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
    print("\n---------------------------------------------"
          "\n")


def login():
    """login screen routine"""
    while True:
        print_divide()
        # prompt user
        login_input = input("Please select an option: "
                            "\n1. Enter Username"
                            "\n2. Return to previous screen"
                            "\n-> ")

        # attempt login
        if login_input == "1":
            name = input("\nUsername -> ")
            pwd = input("Password -> ")

            # authenticate input
            if authenticate(name, pwd) is True:
                # access account
                print("\nSuccess! Opening your account, " + name + ".")
                account(name, pwd)

            else:
                # retry
                print("\nLogin failed. Please enter a valid Username and password.")
                continue

            # if return from successful account login, exit login loop
            break

        # return to previous screen
        if login_input == "2":
            # go back to main screen
            print("\nReturning to previous screen.")
            return

        # invalid entry
        else:
            print("Error! Please enter a valid input.")
            continue


def create_card(user):
    """card creation routine: prompts user to create and add cards to collections."""

    # create flash card routine
    while True:
        card_input = input("\nWelcome to card creation! Please select an option: "
                           "\n1. Create new collection"
                           "\n2. Add card to collection"
                           "\n3. Return to previous screen"
                           "\n-> ")

        if card_input == "1":
            # get collection name and add an empty collection key to the user's collections
            coll_name = input("\nEnter collection name: ")

            # confirm collection
            print("\nYou have entered: " + coll_name)
            finalize = input("\nSave this collection? Y/N: ")

            # save collection
            if finalize.lower() == "y":
                user.add_coll(coll_name)
                input("Collection added! Press any key to return...")

            # do nothing
            elif finalize.lower() == "n":
                print("Collection not saved.")
                continue

        elif card_input == "2":
            # if user has no collections, raise error
            if user.no_cards():
                print("\nYou have no collections! Make a collection first.")
                continue

            else:
                print("\nYour collections: ")
                user.show_coll()
                pos = input("\nSelect a collection to add the card to: ")

                # if user entry is valid, proceed to card creation
                if pos.isdigit() and user.valid_index(pos):

                    # prompt user for front and back
                    front = input("\nPlease enter text for front of card: ")
                    back = input("Please enter text for back of card: ")

                    # confirm card
                    print("\nYou have entered front: " + front + "\nAnd back: " + back)
                    finalize = input("\nSave this card? Y/N: ")

                    # save card
                    if finalize.lower() == "y":
                        user.add_card(pos, front, back)
                        print("Card saved!")

                    # do nothing
                    elif finalize.lower() == "n":
                        print("Card not saved.")
                        continue

                    else:
                        input("Invalid entry. Press any key to return to account...")

                # invalid pos input
                else:
                    input("Invalid entry. Press any key to return to account...")

        # return to previous screen
        elif card_input == "3":
            break

        else:
            input("\nInvalid input! Press any key to return...")
            continue


def account(name, pwd):
    """account page routine"""
    # create user object with credentials
    user = User(name, pwd)

    while True:
        print_divide()
        # prompt user
        account_input = input("Welcome to your FlashCard account! Please enter the number of an option below:"
                              "\n1. View your flash cards - cycles through each card in a collection!"
                              "\n2. Create new flash card - now customizable in just two steps!"
                              "\n3. Edit/delete your flash cards"
                              "\n4. Logoff"
                              "\n5. Help options"
                              "\n-> ")

        # display flash card
        if account_input == "1":
            # if user has no saved flash cards, notify and return to menu
            if user.no_cards():
                print("\nYou currently have no cards to view! Please make a new card from your account menu.")
                input("Press any key to return to the previous screen...")

            # show user's flash cards
            else:
                print("\nShowing a list of all of your collections and their cards: ")
                # print list
                user.show_cards()
                # iterate through each card
                # user.print_front()

                # prompt user for collection to browse
                pos = input("\nEnter the number of the collection you wish to browse: ")

                # if valid entry, browse cards for the given collection
                if pos.isdigit() and user.valid_index(pos):
                    user.print_front(pos)

                # otherwise return to account
                else:
                    input("Invalid entry! Press any key to return to account...")
                    continue

                # notify user end of list has been reached
                input("\nNo more cards to show. Press any key to return to account...")

        # create flash card
        elif account_input == "2":
            # redirect to card creation
            create_card(user)

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
            # first, save data to hdd
            user.save_cards()
            # return to previous menu
            break

        # help menu/invalid entry
        else:
            print("\nWelcome to user account help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to your account page, press any key...")
            continue


def create_account():
    """create a new user account"""
    while True:
        print_divide()
        # prompt user
        create_input = input("Welcome aboard to FlashCard! Please select an option: "
                             "\n1. Select your user name"
                             "\n2. Return to login screen"
                             "\n3. Help options"
                             "\n-> ")

        # display flash card
        if create_input == "1":

            # prompt user for user name and password
            while True:
                # get user name
                user_name = input("\nEnter your new user name: ")
                # check if credential file exists
                cred_file = Path(user_name + ".txt")
                if cred_file.is_file():
                    # print error message
                    print("Error! That user name already exists. Please enter a new choice.")
                    exit_create = input("Or type Q to return to the previous screen: ")

                    # return to account creation screen
                    if exit_create.lower() == "q":
                        break

                    else:
                        continue

                # get user password
                else:
                    user_pwd = input("Please enter a new password: ")

                    # create new user object with input
                    user = User(user_name, user_pwd)

                    # print success notification
                    print("\nAccount creation successful!")
                    input("Logging into your account. Press any key to continue...")

                    # log user into account
                    account(user_name, user_pwd)

                # exit function
                # user will only reach this point after successfully creating a new account,
                # logging in, then logging out
                return

        # return to previous screen
        elif create_input == "2":
            return

        # help menu/invalid input
        else:
            print("\nWelcome to account creation help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to account creation, press any key...")
            continue


if __name__ == '__main__':

    # initialize app
    while True:
        print_divide()

        # main menu prompt
        user_input = input("Welcome to FlashCard! Please choose an option: "
                           "\n1. Login"
                           "\n2. Create new account"
                           "\n3. Exit FlashCard"
                           "\n4. Help options"
                           "\n-> ")

        # go to login screen
        if user_input == "1":
            login()

        # go to new account creation
        elif user_input == "2":
            create_account()

        # terminate program
        elif user_input == "3":
            break

        # all other key entries
        else:
            print("\nWelcome to FlashCard help.")
            print("To navigate, please enter the number of the choice you wish after the -> symbol.")
            print("Any other key entry will bring you to the help menu.")
            input("To return to the main menu, press any key...")
            continue
