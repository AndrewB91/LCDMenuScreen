import MenuScreen
from MenuScreen import Menu
import psutil
from time import sleep



class SysInfo:

    def __init__(self):
        global lcd
        lcd = MenuScreen.lcd

    def run(self):
        lcd.clear()

        while True:
            lcd.clear()
            lcd.message("CPU: " + str(psutil.cpu_percent()) + "%\n")
            lcd.message("RAM: " + str(psutil.virtual_memory()[2]) + "%")
            sleep(1)
            if lcd.buttonPressed(lcd.UP):
                return



MenuScreen.initialise()
menu = Menu("Andrew's\nRaspberry Pi", ["Information", Menu(None, ["System", SysInfo().run]).run])
menu.start()


