from custom.playingcardsscoundrel import Deck
from card_tools import *
from tools import *
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
        self.score = 0
        self.playGame(self.newGame())
    
    def printUI(self):
        print(f"{Fore.RED}❤{self.health}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {self.weapon}{Style.RESET_ALL}:{Fore.CYAN}{self.durability} ⚔ {Style.RESET_ALL}| {Fore.RED}Potion Use:{self.potion_use}{Style.RESET_ALL} | {self.enemies} enemies left")
    def newGame(self):
        """Generates new deck, removes cards for normal-mode"""
        freshdeck = Deck() # generate standard 52-card deck
        remove_cards_normal = ["Ace of Hearts", "Ace of Diamonds", "King of Hearts", "King of Diamonds", "Queen of Hearts", "Queen of Diamonds", "Jack of Hearts", "Jack of Diamonds"]
        deck = remove_cards_from_deck(freshdeck, remove_cards_normal)
        deck.shuffle()
        return deck
    def playGame(self, deck):
        """ Game plays until enemies are 0 or player ends the game"""
        room = deck.draw_n(4)
        
        # Check the room and if the card suit is 0 or 1 (Clubs or Spades) then add 1 to enemies counter.
        for card in room.cards: 
            if card.suit <= 1:
                self.enemies = self.enemies+1

        # Check the deck and if the card suit is 0 or 1 (Clubs or Spades) then add 1 to enemies counter.
        for card in deck.cards: 
            if card.suit <= 1:
                self.enemies = self.enemies+1
        while True:
                # if self has pressed q while game is in session, exit the game session.
                if self.quit_game: 
                    break


                # When self's health is 0 or less, ask if self wants to continue as an Undead or end the game.
                if self.health <= 0 and self.undead == False:
                    print(f"Alas, you have fallen in battle.")
                    print("Continue as an undead? y/n" ) 
                    deathChoice = input().upper()
                    if deathChoice == 'Y':
                        self.undead = True
                        self.calculate_score(deck, room)
                        print("Resurrecting as an undead.")
                    else:
                        self.undead = True
                        self.calculate_score(deck, room)
                        break

                # This is to ensure that a full room is drawn after a Flee is used.
                if self.has_fled == True: 
                    self.has_fled = False
                    drawRoom(deck, room)
                    self.potion_use = 1

                # WIN CONDITION
                elif self.enemies == 0: 
                    if self.undead:
                        print('With no more enemies to attack, you wander aimlessly until another scoundrel appears.')
                        input()
                        break
                    print("You have survived.")
                    print("Congratulations!")
                    self.calculate_score(deck, room)
                    input()
                    break

                # Ensures that the game continues to draw cards so long as there are cards in the "Deck"
                else:
                    if len(room.cards) == 1 and len(deck.cards) != 0: 
                        drawRoom(deck, room)
                        self.potion_use = 1
                        if self.flee_use < 2:
                            self.flee_use = self.flee_use+1 # Flee cooldown

                # So long as there are enemies, we will continue the game.
                while self.enemies >= 1:
                    clear_screen()
                    self.printUI()
                    print(f"{'You are exhausted.' if self.flee_use<2 else 'You feel like you could out run them.'}")
                    print_cards_horizontal(room)
                    print('What would you like to do?')
                    print("a - Attack | w - Wield | p - Use Potion | f - Flee | q - Quit")
                    choice = getchit().upper()
                    match choice:

                        # Attack
                        case 'A':
                            findClubs = find_cards("Clubs", room)
                            findSpades = find_cards("Spades", room)
                            foundEnemies = {key: findClubs[1][key] + findSpades[1][key] for key in findClubs[1]}
                            # Enemy must be present for the condition to pass.
                            if findClubs[0] or findSpades[0]:
                                clear_screen()
                                self.printUI()
                                print("Attacking")
                                print_cards_horizontal(foundEnemies['available'])
                                print(Style.RESET_ALL)
                                print("Select an enemy by typing it's value/rank or press c to cancel")

                                # Input will accept c for cancel, and the rank of the card to target. If the rank isn't present, it is an invalid selection.
                                while True:
                                    try:
                                        enemyChoice = getchit().upper()
                                        if enemyChoice == 'C':
                                            break
                                        selectedEnemy = foundEnemies['rank'].index(enemyChoice)
                                        enemyPosition = foundEnemies['room_position'][selectedEnemy]
                                        enemyStrength = room.cards[enemyPosition].value

                                        # Aces Low into Aces High
                                        if enemyStrength == 1:
                                            enemyStrength = 14
                                        print(f"Your weapon strength is {self.weapon}")
                                        print('The enemy strength is ',enemyStrength)
                                        print(f"The weapon durability is {self.durability}")
                                        print('Use (w)eapon or (b)are hands?')
                                        print('Press c to cancel this action')
                                        break
                                    except:
                                        print("Invalid selection")

                                # Cancel case
                                if enemyChoice == 'C':
                                    break

                                # If a valid rank is selected and the prompt wasn't cancels, we continue to the next loop
                                while True:
                                    weapon = getchit().upper()
                                    match weapon:
                                        case 'W':
                                            try: 
                                                while True:
                                                    if self.weapon == 0:
                                                        print("You don't have a weapon, so you throw hands.")
                                                        getchit()
                                                        weapon = int(self.weapon)
                                                        break

                                                    # With first strike, a weapon can strike any enemy without restriction.
                                                    elif self.first_strike:
                                                        self.durability = enemyStrength
                                                        self.first_strike = False
                                                        print("Your weapon has been damaged")
                                                        print(f"Durability: {self.durability}")
                                                        getchit()
                                                        weapon = int(self.weapon)
                                                        break
                                                    elif enemyStrength < self.durability :
                                                        self.durability = enemyStrength
                                                        weapon = int(self.weapon)
                                                        print("Your weapon has been damaged")
                                                        print(f"Durability: {self.durability}")
                                                        getchit()
                                                        break
                                                    else:
                                                        break
                                                damage = enemyStrength - weapon
                                                if damage <= 0:
                                                    damage = 0
                                                self.health = self.health - damage
                                                room.remove_card(enemyPosition)
                                                self.enemies = self.enemies-1
                                                print(f"Scoundrel takes {damage} damage")
                                                print(f"Health: {self.health}")
                                                input()
                                                break
                                            except:
                                                print("Your weapon would break from this attack.")
                                                print("You will need to use your bare hands or find a new weapon for this monster.")
                                                input()
                                                
                                        case 'B':
                                            weapon = 0
                                            damage = enemyStrength - weapon
                                            if damage <= 0:
                                                damage = 0
                                            self.health = self.health - damage
                                            room.remove_card(enemyPosition)
                                            self.enemies = self.enemies-1
                                            print(f"Scoundrel takes {damage} damage")
                                            print(f"Health: {self.health}")
                                            input()
                                            break
                                        case 'c':
                                            break
                                    break
                            else:
                                print("No Enemies")
                                getchit()
                            break   

                        # Wield Weapon         
                        case 'W':
                            findDiamonds = find_cards("Diamonds", room)
                            foundWeapons = findDiamonds[1]
                            if findDiamonds[0]:
                                clear_screen()
                                self.printUI()
                                print("Wield a weapon")
                                print_cards_horizontal(foundWeapons['available'])
                                print(Style.RESET_ALL)
                                print("Select a weapon by typing it's rank or enter c to cancel")
                                while True:
                                    weaponChoice = getchit().upper()
                                    if weaponChoice == 'C':
                                            break
                                    if weaponChoice in foundWeapons['rank']:
                                        selectedWeapon = foundWeapons['rank'].index(weaponChoice)
                                        weaponPosition = foundWeapons['room_position'][selectedWeapon]
                                        weaponStrength = room.cards[weaponPosition].value
                                        self.weapon = weaponStrength
                                        self.durability = 14
                                        self.first_strike = True
                                        room.remove_card(weaponPosition)
                                        break

                            else:
                                print("No weapons available")
                                getchit()
                            break

                        # Use Potion
                        case 'P':
                            findHearts = find_cards("Hearts", room)
                            foundPotions = findHearts[1]
                            if findHearts[0]:
                                clear_screen()
                                self.printUI()
                                print("Drink a potion")
                                print_cards_horizontal(foundPotions['available'])
                                print(Style.RESET_ALL)
                                if self.potion_use == 0:
                                    print("\033[4mYou can drink another potion, but it will have no effect.\033[0m")
                                print("Select a potion by typing it's rank or enter c to cancel")
                                while True:
                                    try:
                                        potionChoice = getchit().upper()
                                        if potionChoice == 'C':
                                            break
                                        selectedPotion = foundPotions["rank"].index(potionChoice)
                                        potionPosition = foundPotions["room_position"][selectedPotion]
                                        potionStrength = room.cards[potionPosition].value
                                        if potionChoice in foundPotions['rank'] and self.potion_use > 0 :
                                            self.health = self.health + potionStrength
                                            print(f"This potion heals for {potionStrength} health.")
                                            print(f"Your health is now {self.health}")
                                            getchit()
                                            self.potion_use = 0
                                            room.remove_card(potionPosition)
                                            break
                                        else:
                                            room.remove_card(potionPosition)
                                            break
                                    except:
                                        print("That potion is not available.")
                        
                            else:
                                print("No potions available")
                                getchit()
                                
                            break

                        # Flee Room
                        case 'F':
                            if self.flee_use < 2:
                                print("You are exhausted and cannot flee.")
                                getchit()
                            else:
                                print("You have fled. All cards have been moved to the bottom of the deck.")
                                getchit()
                                self.flee_use = 0
                                self.has_fled = True
                                for card in room.cards:
                                    deck.cards.insert(0, card)
                                room.cards.clear()
                                break

                        # Quit Game
                        case 'Q':
                            print("Are you sure you want to quit? y/n")
                            quitChoice = getchit().upper()
                            if quitChoice == "Y":
                                self.undead = True
                                self.quit_game = True
                            break
    def calculate_score(self, deck, room):
        if self.undead:
            find_room_clubs = find_cards("Clubs", room)
            find_room_spades = find_cards("Spades", room)
            find_deck_clubs = find_cards("Clubs", deck)
            find_deck_spades = find_cards("Spades", deck)
            found_enemies = {
                key: find_room_clubs[1][key] + 
                find_room_spades[1][key] + 
                find_deck_clubs[1][key] + 
                find_deck_spades[1][key] 
                for key in find_room_clubs[1]
                }
            for enemy in found_enemies['value']:
                if enemy == 1:
                    enemy = 14
                self.score = self.score - enemy
            print(f"Final Score: {self.score}")
            return self.score
        else:
            find_room_potions = find_cards("Hearts", room)
            find_deck_potions = find_cards("Hearts", deck)
            found_potions = {key: find_room_potions[1][key]+find_deck_potions[1][key] for key in find_room_potions[1]}
            self.score = self.health
            print(f"Health Score: {self.score}")
            for potion in found_potions['value']:
                print(f"Potion Bonus! +{potion} points")
                self.score = self.score + potion
            print(f"Final Score: {self.score}")
            return self.score
