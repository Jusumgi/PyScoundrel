from tools import *
from card_tools import *
from Game import Game
score_history = []
def mainMenu():
    high_score = max(score_history)
    while True:
        # clear_screen()
        print(f"Welcome to Scoundrel | High Score: {high_score}")
        print("Press 1 to Start")
        print("Press 2 for Rules/About")
        print("Press q to Quit")
        response = getchit()
        match response:
            case '1':
                gameInstance = Game()
                if not gameInstance.quit_game:
                    score_history.append(gameInstance.score)
            case '2':
                clear_screen()
                print("Scoundrel is a single-player Rogue-like card game by Zach Gage and Kurt Bieg")
                print("Press 'H' for the original rules to Scoundrel, which will open a PDF in your web browser.")
                print("\033[4mHouse Rules/Changes\033[0m")
                print("Flee can be used at any point within a room, with the same cooldown of 2 rooms.")
                print("\033[4mUI\033[0m")
                print("❤ Health ❤| ⚔ Weapon:Durability ⚔")
                print("\033[4mGeneral Rules\033[0m")                
                print("* Health maximum is 20. Once health reaches 0, the game ends and your score is tallied based on the value of each remaining enemy as a negative score.")
                print("* Weapons block incoming damage and when initially equipped have 'first strike' which allows you to hit any enemy.")
                print("* After an enemy has been hit with a weapon, the player incurs Durability where the next enemy struck must be less than the strength/rank of the monster before it.")
                print("* Potions can effectively be used once per room. Any other potions used in the same room have no effect and are wasted/discarded.")
                pdfcall = getchit().upper()
                if pdfcall == 'H':
                    open_pdf('Scoundrel.pdf')
            case 'q':
                break
mainMenu()

