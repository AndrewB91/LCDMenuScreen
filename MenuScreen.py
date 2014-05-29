from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep

global lcd

def initialise():
    global lcd
    lcd = Adafruit_CharLCDPlate()



# Menu class takes in any number of parameters, each of which is an array consisting of a string heading,
# and a method which will be called if the option is selected. Menus may be supplied as parameters to other menus.
class Menu:
    def __init__(self, welcome_message, *options):
        # Keep track of the supplied options
        self.options = []
        for option in options:
            self.options.append(option)

        self.top_level = welcome_message is not None

        if self.top_level:
            self.options.append(["Sleep", DimScreen])
            self.options.append(["Quit", Menu(None, ["Are you sure?\n     <Yes>", Quit], ["Are you sure?\n     <No>", None]).run])

        self.max_option = len(self.options) - 1
        self.current_option = 0

        global screen_on
        screen_on = True

        # Assign the welcome message
        self.welcome_message = welcome_message


    def start(self):
        # Clear and switch on the LCD
        lcd.clear()
        lcd.backlight(lcd.ON)

        # Display the welcome message, sleep, and then run the menu screen
        if self.welcome_message != None:
            self.display_message(self.welcome_message)
            sleep(2)

        self.run()

    @staticmethod
    def display_message(message):
        lcd.clear()
        lcd.message(message)

    def display_option(self):
        Menu.display_message(self.options[self.current_option][0])

    def run(self):
        global screen_on
        cycleNumber = 0

        self.display_option()
        sleep(0.2)

        while True:
            if not screen_on:
                sleep(3)
                if lcd.buttonPressed(lcd.SELECT):
                    cycleNumber = 0
                    lcd.clear()
                    lcd.backlight(lcd.ON)
                    screen_on = True
                    self.display_option()
                    sleep(0.5)
            elif lcd.buttonPressed(lcd.LEFT):
                cycleNumber = 0
                self.left()
            elif lcd.buttonPressed(lcd.RIGHT):
                cycleNumber = 0
                self.right()
            elif lcd.buttonPressed(lcd.SELECT):
                cycleNumber = 0
                if self.select() == -1:
                    sleep(0.2)
                    return
                if screen_on:
                    self.display_option()
            elif lcd.buttonPressed(lcd.UP) and not self.top_level:
                sleep(0.5)
                if lcd.buttonPressed(lcd.UP):
                    return
            elif cycleNumber > 3000:
                DimScreen()
            else:
                cycleNumber += 1
                sleep(0.01)




    def left(self):
        if self.current_option != 0:
            self.current_option -= 1
        self.display_option()
        sleep(0.2)

    def right(self):
        if self.current_option != self.max_option:
            self.current_option += 1
        self.display_option()
        sleep(0.2)

    def select(self):
        if (self.options[self.current_option])[1] is None:
            return -1
        return (self.options[self.current_option])[1]()


def DimScreen():
    lcd.clear()
    lcd.backlight(lcd.OFF)
    global screen_on
    screen_on = False

def Quit():
    DimScreen()
    exit()
