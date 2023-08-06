import pyautogui
import time


class ReadFile:
    def __init__(self, file):
        self.file = file

    def spam(self):
        f = open(self.file, "r")

        print("""
╔═══╗─────────╔══╗───╔╗
║╔═╗║─────────║╔╗║──╔╝╚╗
║╚══╦══╦══╦╗╔╗║╚╝╚╦═╩╗╔╝
╚══╗║╔╗║╔╗║╚╝║║╔═╗║╔╗║║
║╚═╝║╚╝║╔╗║║║║║╚═╝║╚╝║╚╗
╚═══╣╔═╩╝╚╩╩╩╝╚═══╩══╩═╝
────║║
────╚╝
	""")

        print("To stop the program, move the curser to the upper left corner of the screen.")
        print("")

        print("Starting in 5...")
        time.sleep(1)
        print("Starting in 4...")
        time.sleep(1)
        print("Starting in 3...")
        time.sleep(1)
        print("Starting in 2...")
        time.sleep(1)
        print("Starting in 1...")
        time.sleep(1)
        print("Boom!")

        for line in f:
            pyautogui.typewrite(line)
            pyautogui.press("enter")


def spam(msg, count):

    print("""
╔═══╗─────────╔══╗───╔╗
║╔═╗║─────────║╔╗║──╔╝╚╗
║╚══╦══╦══╦╗╔╗║╚╝╚╦═╩╗╔╝
╚══╗║╔╗║╔╗║╚╝║║╔═╗║╔╗║║
║╚═╝║╚╝║╔╗║║║║║╚═╝║╚╝║╚╗
╚═══╣╔═╩╝╚╩╩╩╝╚═══╩══╩═╝
────║║
────╚╝
""")

    print("To stop the program, move the curser to the upper left corner of the screen.")
    print("")

    print("Starting in 5...")
    time.sleep(1)
    print("Starting in 4...")
    time.sleep(1)
    print("Starting in 3...")
    time.sleep(1)
    print("Starting in 2...")
    time.sleep(1)
    print("Starting in 1...")
    time.sleep(1)
    print("Boom!")

    for _ in range(int(count)):
        pyautogui.typewrite(msg)
        pyautogui.press("enter")
