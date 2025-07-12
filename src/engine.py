import time
import random
import os
import cliEngine.cliEngine as cl
import json
import curses
import sys

class Engine():
    def __init__(self, name, author, saveDataFile="saveData.json"):
        self.name = name
        self.author = author
        self.saveDataFile = saveDataFile
        
    def setTerminalSize(self, width, height):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width))
        sys.stdout.flush() # Important to flush the buffer
    
    def remove_after_word(self, st, word):
        parts = st.split()
        if word in parts:
            index = parts.index(word)
            return ' '.join(parts[:index])
        return st  # if word not found, return original string

    def handleInput(self):
        """
        Robbed from cliEngine, this function allows
        for the user to only input a single letter.

        Returns:
            str: Letter given by user
        """
        return cl.inputReceiver(1)
    
    def clearScreen(self):
        """
        Clears the screen for UNIX.
        """
        os.system("clear")

    def sleep(self, t: int):
        """
        Using time.sleep(), slows
        down the progress by a given
        amount.

        Args:
            t (int): Seconds to slow down.
        """
        time.sleep(t)
    
    def randomness(self, mins: int, maxs: int):
        """
        Returns a random number by the min and max
        values given by the user.

        Args:
            mins (int): Mininum number to be generated.
            maxs (int): Maxinum number to be generated

        Returns:
            int: Random number generated.
        """
        return random.randint(mins, maxs)
    
    def spriteHandler(self, sourcefile):
        """
        Loads sprites from file and returns
        them in a string.

        Args:
            sourcefile (str): File where sprite is stored

        Returns:
            str: Sprite from file.
        """
        with open(sourcefile, "r") as f:
            spriteTable = f.readlines()
        
        spriteString = ""
        for line in spriteTable:
            spriteString += f"{line}"
        
        return spriteString

    def saveData(self, data: dict):
        """
        Saves data from a dictionary
        given by argument in a file
        determined by __init__

        Args:
            data (dict): Data you want to store.
        """
        with open(self.saveDataFile, "w") as saveDataFiler:
            json.dump(data, saveDataFiler)

    def loadData(self):
        """
        Loads data from the file given
        and returns a dict.

        Returns:
            dict: Data restored.
        """
        with open(self.saveDataFile, "r") as loadDatar:
            return json.load(loadDatar)
        
    def selectMenu(self, options):
        def inner(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(True)
            selected = 0
            delay = 0.05

            # Prepare display options
            display_options = [f"{i + 1}.- {opt.capitalize()}" for i, opt in enumerate(options)]

            while True:
                stdscr.clear()
                h, w = stdscr.getmaxyx()
                max_visible = h - 2

                if selected < max_visible // 2:
                    start_index = 0
                elif selected > len(display_options) - max_visible // 2:
                    start_index = len(display_options) - max_visible
                else:
                    start_index = selected - max_visible // 2

                start_index = max(0, min(start_index, len(display_options) - max_visible))
                visible_options = display_options[start_index:start_index + max_visible]

                for i, option in enumerate(visible_options):
                    actual_index = start_index + i
                    prefix = "> " if actual_index == selected else "  "
                    x = w // 2 - len(option) // 2
                    y = i + 1
                    stdscr.addstr(y, x, prefix + option[:w - 4])

                stdscr.refresh()
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    selected = (selected - 1) % len(options)
                elif key == curses.KEY_DOWN:
                    selected = (selected + 1) % len(options)
                elif key in [curses.KEY_ENTER, 10, 13]:
                    return selected  # ✅ Return the index instead of the string

                time.sleep(delay)

        return curses.wrapper(inner)
    
    def Credits(self, delay=True):
        def sleep():
            if delay:
                time.sleep(0.3)

        print(self.name)
        sleep()
        print(f"Developed by {self.author}")
        sleep()
        print(" ")
        print("Be sure to save before quitting")
        sleep()
        print(" ")
        sleep()
        print(" ")
        sleep()
