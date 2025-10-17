from card_tools import *
from colorama import Fore, Style
class Game:
    def __init__(self):
        self.health = 20
        self.weapon = 0
        self.first_strike = False
        self.durability = 14
        self.potion_use = 1
        self.flee_use = 2
        self.has_fled = False
        self.undead = False
        self.quit_game = False
        self.enemies = 0
    
    def printUI(self):
        print(f"{Fore.RED}❤ {self.health}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {self.weapon}{Style.RESET_ALL}:{Fore.CYAN}{self.durability} ⚔ {Style.RESET_ALL}| {self.enemies} enemies left")