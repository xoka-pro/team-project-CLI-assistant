from functions import *


def main():
    """ Main function - all interaction with user """
    startup_loader()
    print(hello())
    meow = 0
    while True:
        msg = input("Input command: ")
        command, params = parser(msg)
        if command:
            print(command(*params))
            meow += 1
            if meow == 4:
                print('Meow!')
                meow = 0
        else:
            print(incorrect_input(msg))


if __name__ == '__main__':
    main()
