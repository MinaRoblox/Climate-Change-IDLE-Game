# Climate Change IDLE Game
A simple IDLE game developed for the terminal made in Python as a graduation project.
### Warning, when you first launch the game, make sure to select "Erase data", as the game will crash without a saveData.json file.

## Features
- Save and loading using JSON
- Fully developed in the terminal
- Custom sprites

## Playing the game
Currently, there are 2 ways to play CCIG: Building, Uncompiled and Releases version.


### Releases
Download the latest version of CCIG in the Releases tab of your platform
CCIG -- macOS/Linux
CCIG.exe -- Windows

### Building
To build the project, you'll need pyinstaller. Firstly, install the required libraries in
requirements.txt, and then compile with this command:
~~~sh
pyinstaller -F -n CCIG game.py
~~~

### Uncompiled
Install the required libraries of requirements.txt and run game.py.
