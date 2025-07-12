from src.engine import Engine

class ClimateChangeIDLEGame:
    def __init__(self):
        self.ENGINE = Engine("Climate Change Clicker", "minaroblox")
        # this doesn't work # self.ENGINE.setTerminalSize(100, 100)
        self.TOTAL_VALUE = 0
        self.AMBIENT_SPRITE = "images/ambient.txt"
        self.DOLLAR_SPRITE = "images/dollar_sprite.txt"
        self.MENU_SPRITE = "images/menu.txt"
        self.AMBIENT_SPR = self.ENGINE.spriteHandler(self.AMBIENT_SPRITE)
        self.DOLLAR_SPR = self.ENGINE.spriteHandler(self.DOLLAR_SPRITE)
        self.MENU_SPRITE_SPR = self.ENGINE.spriteHandler(self.MENU_SPRITE)
        self.KEYS = {
            "Increment": "w",
            "Store": "d",
            "Quit": "q"
        }
        self.CPS = 0
        self.INCREASE_PERCENTAGE = 0 # Used in increment() and auto_increment()
        self.CPS_UPGRADES_PRICES = [
            500,
            2000,
            5000,
            8000,
            20000,
            100000,
            500000,
        ]
        self.CPS_UPGRADES_AVAILIBLE = [
            f"3 CPS for {self.CPS_UPGRADES_PRICES[0]}",
            f"6 CPS for {self.CPS_UPGRADES_PRICES[1]}",
            f"10 CPS for {self.CPS_UPGRADES_PRICES[2]}",
            f"20 CPS for {self.CPS_UPGRADES_PRICES[3]}",
            f"40 CPS for {self.CPS_UPGRADES_PRICES[4]}",
            f"100 CPS for {self.CPS_UPGRADES_PRICES[5]}",
            f"200 CPS for {self.CPS_UPGRADES_PRICES[6]}",
            "Go back."
        ]
        self.CPS_UPGRADES_UNLOCKED = []
        self.PERCENTAGE_UPGRADES_PRICES = [
            1000,
            5000,
            10000,
            50000,
            1000000,
            5000000,
            99999999
        ]
        self.PERCENTAGE_UPGRADES_AVAILIBLE = [
            f"100 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[0]}",
            f"200 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[1]}",
            f"400 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[2]}",
            f"500 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[3]}",
            f"6000 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[4]}",
            f"8000 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[5]}",
            f"10000 % Increase for {self.PERCENTAGE_UPGRADES_PRICES[6]}",
            "Go back."
        ]
        self.PERCENTAGE_UPGRADES_UNLOCKED = []
        self.debug = True

    def increment(self):
        """
        Uses self.INCREASE_PERCENTAGE and self.TOTAL_VALUE
        """ 

        self.TOTAL_VALUE += 1 + (self.INCREASE_PERCENTAGE / 100)
    
    def saveData(self):
        self.SAVE_DATA = {
            "Total Value": self.TOTAL_VALUE,
            "CPS": self.CPS,
            "Percentage Increase": self.INCREASE_PERCENTAGE,
            "CPS Upgrades Availible": self.CPS_UPGRADES_AVAILIBLE,
            "CPS Upgrades Unlocked": self.CPS_UPGRADES_UNLOCKED,
            "Percentage Upgrades Availible": self.PERCENTAGE_UPGRADES_AVAILIBLE,
            "Percentage Upgrades Unlocked": self.PERCENTAGE_UPGRADES_UNLOCKED   
        }
        self.ENGINE.saveData(self.SAVE_DATA)

    def loadData(self):
        data = self.ENGINE.loadData()
        try:
            if isinstance(data, dict):
                self.TOTAL_VALUE = data["Total Value"]
                self.CPS = data["CPS"]
                self.INCREASE_PERCENTAGE = data["Percentage Increase"]
                self.CPS_UPGRADES_UNLOCKED = data["CPS Upgrades Unlocked"]
                self.CPS_UPGRADES_AVAILIBLE = data["CPS Upgrades Availible"]
                self.PERCENTAGE_UPGRADES_AVAILIBLE = data["Percentage Upgrades Availible"]
                self.PERCENTAGE_UPGRADES_UNLOCKED = data["Percentage Upgrades Unlocked"]

        except:
            pass
            
    def calculateCPSIncrease(self):
        """
        Uses self.CPS_UPGRADES_UNLOCKED and self.CPS
        """
        try:
            if self.CPS < int(self.ENGINE.remove_after_word(self.CPS_UPGRADES_UNLOCKED[-1], "CPS")):
                self.CPS = int(self.ENGINE.remove_after_word(self.CPS_UPGRADES_UNLOCKED[-1], "CPS"))
            else:
                pass
        except:
            pass
    
    def calculatePercentageIncrease(self):
        """
        Uses self.PERCENTAGE_UPGRADES_AVAILIBLE and self.INCREASE_PERCENTAGE
        """
        try:
            if self.INCREASE_PERCENTAGE < int(self.ENGINE.remove_after_word(self.PERCENTAGE_UPGRADES_UNLOCKED[-1], "%")):
                self.INCREASE_PERCENTAGE = int(self.ENGINE.remove_after_word(self.PERCENTAGE_UPGRADES_UNLOCKED[-1],"%"))
            else:
                pass
        except:
            pass

    def handlePurchase(self, item: int, itemType: str):
        """
        Handles a purchase.

        Args:
            item (int): Item wanting to purchase (Position in array)
            itemType (str): Determines if percentage or cps purchase.
        """
        
        if itemType == "CPS":
            # TOTAL_VALUE
            # CPS_UPGRADES_AVAILIBLE
            # CPS_UPGRADES_UNLOCKED
            # CPS_UPGRADES_PRICES
            itemPrice = self.CPS_UPGRADES_PRICES[item]
            if self.TOTAL_VALUE >= itemPrice:
                self.TOTAL_VALUE -= itemPrice
                self.CPS_UPGRADES_UNLOCKED.append(self.CPS_UPGRADES_AVAILIBLE[item])
                self.CPS_UPGRADES_AVAILIBLE.remove(self.CPS_UPGRADES_AVAILIBLE[item])
                self.calculateCPSIncrease()
            else:
                return False

        elif itemType == "%":
            # TOTAL_VALUE
            # self.PERCENTAGE_UPGRADES_AVAILIBLE
            # self.PERCENTAGE_UPGRADES_UNLOCKED
            # self.PERCENTAGE_UPGRADES_PRICES
            itemPrice = self.PERCENTAGE_UPGRADES_PRICES[item]
            if self.TOTAL_VALUE >= itemPrice:
                self.TOTAL_VALUE -= itemPrice
                self.PERCENTAGE_UPGRADES_UNLOCKED.append(self.PERCENTAGE_UPGRADES_AVAILIBLE[item])
                self.PERCENTAGE_UPGRADES_AVAILIBLE.remove(self.PERCENTAGE_UPGRADES_AVAILIBLE[item])
                self.calculatePercentageIncrease()
            else:
                return False
            
    def autoIncrement(self):
        """
        Uses self.CPS and self.PERCENTAGE_INCREASE
        Goal of this is to run every second and use the upgrades
        purchased to determine how much is incremented.
        """
        if self.CPS > 0:
            self.TOTAL_VALUE += self.CPS + (self.INCREASE_PERCENTAGE / 100)

    def menu(self):
        """
        Leader to exit() and game()
        """
        print(self.MENU_SPRITE_SPR)
        self.ENGINE.Credits(delay=True)
        def chooseSelection():
            print(" ")
            print("1. Start")
            print("2. Information")
            print("3. Erase data.")
            print("4. Quit.")
            print("5. Print this text.")
            print(" ")
        chooseSelection()
        while True:
            print("Make your selection in numbers")
            try:
                numberOptionChosen = int(input("> "))
                match numberOptionChosen:
                    case 5:
                        chooseSelection()
                    case 1:
                        self.ENGINE.clearScreen()
                        break
                    case 2:
                        print("Unavailible!")
                        print(" ")
                    case 3:
                        data = {

                        }
                        self.ENGINE.saveData(data)
                        print("Data erasen!")
                    case 4:
                        exit()
            except:
                print("Enter a number!")

        self.game() # Start of game loop

    def game(self):
        """
        Holder of game loop
        """
        # Default engine() thingy
        loop = True
        exitLoop = False

        # Load data
        self.loadData()
        while loop:
            if exitLoop:
                self.saveData()
                break 
            
            self.ENGINE.clearScreen()
            print(self.AMBIENT_SPR)
            print(f"CURRENT VALUE: {self.TOTAL_VALUE}")
            print(f"CPS PURCHASED: {self.CPS_UPGRADES_UNLOCKED}")
            print(f"% PURCHASED: {self.PERCENTAGE_UPGRADES_UNLOCKED}")
            print(f"CPS: {self.CPS}")
            print(f"%: {self.INCREASE_PERCENTAGE}")
            userInput = self.ENGINE.handleInput()
            if userInput == self.KEYS["Quit"]:
                exitLoop = True
                continue
            elif userInput == self.KEYS["Increment"]:
                self.increment()
                self.autoIncrement()
                continue
            elif userInput == self.KEYS["Store"]:
                self.store()
                
            self.autoIncrement()

    def store(self):
        """
        Store to buy upgrades
        Last part to finish
        """
        # The exiting part is going back to the game
        while True:
            self.ENGINE.clearScreen()
            print(self.DOLLAR_SPR)
            print("Welcome to the SHOP")
            print("Choose a select category for upgrading.")
            print(" ")
            print("1.- Clicks per second.")
            print("2.- Percentage Increase.")
            print(f"Enter anything other than a number without decimals to go to the game")
            try:
                uI = int(input("> "))
                if uI == 1:
                    c = self.ENGINE.selectMenu(self.CPS_UPGRADES_AVAILIBLE)
                    if c == 8 - 1:
                        pass
                    else:
                        check = self.handlePurchase(c, "CPS")
                        if check == False:
                            print("Not enough money!")
                            self.ENGINE.sleep(1)
                elif uI == 2:
                    c = self.ENGINE.selectMenu(self.PERCENTAGE_UPGRADES_AVAILIBLE)
                    if c == 8 - 1:
                        pass
                    else:
                        check = self.handlePurchase(c, "%")
                        if check == False:
                            print("Not enough money!")
                            self.ENGINE.sleep(1)

            except:
                break
def run():
    game = ClimateChangeIDLEGame()
    game.menu()

if __name__ == "__main__":
    run()
