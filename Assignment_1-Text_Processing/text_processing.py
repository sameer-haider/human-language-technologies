import sys
import os
import re
import pickle


# def openfile(filepath):
#     with open(os.path.join(os.getcwd(), filepath), 'r') as f:
#         text_in = f.read()
#     print(text_in)

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee ID:", self.id)
        print("\t", self.first, self.mi, self.last)


def process_input(filepath):
    persons = {}
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        # Skip the first line
        next(f)
        for line in f:
            # Split on comma
            fields = line.strip().split(',')

            # Capitalize first and last name
            fields[0] = fields[0].capitalize()
            fields[1] = fields[1].capitalize()

            # Capitalize MI or save as X if none
            if not fields[2]:
                fields[2] = 'X'
            else:
                fields[2].upper()

            # Check ID, ask user to fix if wrong
            id_format = re.compile("^[A-Z]{2}[0-9]{4}$")
            while not id_format.match(fields[3]):
                print("ID is invalid: ", fields[3])
                print("ID is 2 letters followed by 4 digits.")
                fields[3] = input("Please enter a valid ID: ")

            # Check phone number, ask user to fix if wrong
            phone_format = re.compile("^[0-9]{3}-[0-9]{3}-[0-9]{4}$")
            while not phone_format.match(fields[4]):
                print("Phone number is invalid: ", fields[4])
                print("Phone number should look like this: 123-456-7890")
                fields[4] = input("Please enter a valid phone number: ")

            # Create a Person object and add it to the dict
            person = Person(fields[0], fields[1], fields[2], fields[3], fields[4])
            if fields[3] in persons:
                print("Error: Duplicate ID.")
            else:
                persons[fields[3]] = person

    return persons


def main():
    # Check if data arg
    if len(sys.argv) < 2:
        print("Error: No file specified.")
        return

    filepath = sys.argv[1]
    persons = process_input(filepath)

    # Save dict as a pickle file
    with open('persons.pickle', 'wb') as file:
        pickle.dump(persons, file)

    # Read pickle file and display persons
    with open('persons.pickle', 'rb') as file:
        pickleread = pickle.load(file)
        for person in pickleread.values():
            person.display()


if __name__ == '__main__':
    main()
