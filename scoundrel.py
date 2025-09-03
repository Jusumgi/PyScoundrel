from custom.playingcardsscoundrel import Deck
from colorama import Fore, Style
from tools import *

def newGame():
    # Generates new deck, removes cards for normal-mode
    freshdeck = Deck() # generate standard 52-card deck
    remove_cards_normal = ["Ace of Hearts", "Ace of Diamonds", "King of Hearts", "King of Diamonds", "Queen of Hearts", "Queen of Diamonds", "Jack of Hearts", "Jack of Diamonds"]
    deck = remove_cards_from_deck(freshdeck, remove_cards_normal)
    deck.shuffle()
    return deck

def playGame(deck):
    player = {
        'health': 20,
        'weapon': 0,
        'firststrike': False,
        'durability': 14,
        'potionUse': 1,
        'fleeUse': 2,
        'hasFled': False,
        'undead': False,
        'quitGame': False
    }
    
    room = deck.draw_n(4)
    
    while True:
        # try:
            if player['quitGame']:
                break
            enemies = 0 # Enemy counter is tracked to determine when the game is over (as a win condition). Will have to change this when Scoring is implemented
            for card in room.cards:
                if card.suit <= 1:
                    enemies = enemies+1
            for card in deck.cards:
                if card.suit <= 1:
                    enemies = enemies+1
            if player['health'] <= 0 and player['undead'] == False:
                print(f"Alas, you have fallen in battle.")
                print("Continue as an undead? y/n" ) #placeholder/option to keep playing to see if you can come back to positive HP
                deathChoice = lowerisUpper(input())
                if deathChoice == 'Y':
                    player['undead'] = True
                    print("Resurrecting as an undead.")
                else:
                    break
            if player['hasFled'] == True: # This is to ensure that a full room is drawn after a Flee is used.
                player['hasFled'] = False
                drawRoom(deck, room)
                player['potionUse'] = 1
            elif enemies == 0: # The only win condition
                if player['undead']:
                    print('With no more enemies to attack, you wander aimlessly until another scoundrel appears.')
                    input()
                    break
                print("You have survived.")
                print("Congratulations!")
                input()
                break
            else:
                if len(room.cards) == 1 and len(deck.cards) != 0: # ensures that the game continues to draw cards so long as there are cards in the "Deck"
                    drawRoom(deck, room)
                    player['potionUse'] = 1
                    if player['fleeUse'] < 2:
                        player['fleeUse'] = player['fleeUse']+1
            while enemies >= 1:
                clear_screen()
                print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                print(f"{'You are exhausted.' if player['fleeUse']<2 else 'You feel like you could out run them.'}")
                print_cards_horizontal(room)
                print('What would you like to do?')
                print("a - Attack | w - Wield | p - Use Potion | f - Flee | q - Quit")
                # try:
                choice = getchit()
                match choice:
                    case 'a':
                        foundEnemy = False
                        foundEnemies = {
                            'available': [],
                            'value': [],
                            'suit': [],
                            'room_position': []
                        }
                        for index, card in enumerate(room.cards):
                            if card.suit_name == 'Clubs' or card.suit_name == 'Spades':
                                foundEnemy = True
                                foundEnemies["available"].append(card)
                                foundEnemies["value"].append(str(card.rank)[0])
                                foundEnemies['suit'].append(str(card.suit_name)[0])
                                foundEnemies['room_position'].append(index)
                        if foundEnemy:
                            clear_screen()
                            print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                            print("Attacking")
                            print_cards_horizontal(foundEnemies['available'])
                            print(Style.RESET_ALL)
                            print("Select an enemy by typing it's value/rank or press c to cancel")
                            while True:
                                try:
                                        enemyChoice = lowerisUpper(getchit())
                                        if enemyChoice == 'C':
                                            break
                                        selectedEnemy = foundEnemies["value"].index(enemyChoice)
                                        enemyPosition = foundEnemies["room_position"][selectedEnemy]
                                        enemyStrength = room.cards[enemyPosition].value
                                        if enemyStrength == 1:
                                            enemyStrength = 14
                                        print(f"Your weapon strength is {player['weapon']}")
                                        print('The enemy strength is ',enemyStrength)
                                        print(f"The weapon durability is {player['durability']}")
                                        print('Use (w)eapon or (b)are hands?')
                                        print('Press c to cancel this action')
                                        break
                                except:
                                    print("Invalid selection")
                            if enemyChoice == 'C':
                                break
                            while True:
                                weapon = getchit()
                                match weapon:
                                    case 'w':
                                        try: 
                                            while True:
                                                if player['weapon'] == 0:
                                                    print("You don't have a weapon, so you throw hands.")
                                                    getchit()
                                                    weapon = int(player['weapon'])
                                                    break
                                                elif player['firststrike']:
                                                    player['durability'] = enemyStrength
                                                    player['firststrike'] = False
                                                    print("Your weapon has been damaged")
                                                    print(f"Durability: {player['durability']}")
                                                    getchit()
                                                    weapon = int(player['weapon'])
                                                    break
                                                elif enemyStrength < player['durability'] :
                                                    player['durability'] = enemyStrength
                                                    weapon = int(player['weapon'])
                                                    print("Your weapon has been damaged")
                                                    print(f"Durability: {player['durability']}")
                                                    getchit()
                                                    break
                                                else:
                                                    break
                                            
                                            if enemyStrength == 1:
                                                damage = 14 - weapon
                                                player['health'] = player['health'] - damage
                                            else:
                                                damage = enemyStrength - weapon
                                            if damage <= 0:
                                                damage = 0
                                            player['health'] = player['health'] - damage
                                            room.remove_card(enemyPosition)
                                            print(f"Player takes {damage} damage")
                                            print(f"Health: {player['health']}")
                                            input()
                                            break
                                        except:
                                            print("Your weapon would break from this attack.")
                                            input()
                                            
                                    case 'b':
                                        weapon = 0
                                        if enemyStrength == 1:
                                            damage = 14 - weapon
                                            player['health'] = player['health'] - damage
                                        else:
                                            damage = enemyStrength - weapon
                                        if damage <= 0:
                                            damage = 0
                                        player['health'] = player['health'] - damage
                                        room.remove_card(enemyPosition)
                                        print(f"Scoundrel takes {damage} damage")
                                        print(f"Health: {player['health']}")
                                        input()
                                        break
                                    case 'c':
                                        break
                                break
                        if not foundEnemy:
                            print("No Enemies")
                            getchit()
                        break                
                    case 'w':
                        foundWeapon = False
                        foundWeapons = {
                            'available': [],
                            'value': [],
                            'room_position': []
                        }
                        for index, card in enumerate(room.cards):
                            if card.suit_name == 'Diamonds':
                                foundWeapon = True
                                foundWeapons["available"].append(card)
                                foundWeapons["value"].append(str(card.rank))
                                foundWeapons['room_position'].append(index)
                        if foundWeapon:
                            clear_screen()
                            print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                            print("Wield a weapon")
                            print_cards_horizontal(foundWeapons['available'])
                            print(Style.RESET_ALL)
                            print("Select a weapon by typing it's rank or enter c to cancel")
                            while True:
                                weaponChoice = lowerisUpper(getchit())
                                if weaponChoice == 'C':
                                        break
                                if weaponChoice in foundWeapons['value']:
                                    selectedWeapon = foundWeapons["value"].index(weaponChoice)
                                    weaponPosition = foundWeapons["room_position"][selectedWeapon]
                                    weaponStrength = room.cards[weaponPosition].value
                                    player["weapon"] = weaponStrength
                                    player["durability"] = 14
                                    player['firststrike'] = True
                                    room.remove_card(weaponPosition)
                                    break

                        else:
                            print("No weapons available")
                            getchit()
                        break
                    case 'p':
                        foundPotion = False
                        foundPotions = {
                            'available': [],
                            'value': [],
                            'room_position': []
                        }
                        
                        for index, card in enumerate(room.cards):
                            if card.suit_name == 'Hearts':
                                foundPotion = True
                                foundPotions["available"].append(card)
                                foundPotions["value"].append(str(card.rank))
                                foundPotions['room_position'].append(index)
                        if foundPotion:
                            clear_screen()
                            print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                            print("Drink a potion")
                            print_cards_horizontal(foundPotions['available'])
                            print(Style.RESET_ALL)
                            if player['potionUse'] == 0:
                                print("\033[4mYou can drink another potion, but it will have no effect.\033[0m")
                            print("Select a potion by typing it's rank or enter c to cancel")
                            while True:
                                try:
                                    potionChoice = lowerisUpper(getchit())
                                    if potionChoice == 'C':
                                        break
                                    selectedPotion = foundPotions["value"].index(potionChoice)
                                    potionPosition = foundPotions["room_position"][selectedPotion]
                                    potionStrength = room.cards[potionPosition].value
                                    if potionChoice in foundPotions['value'] and player['potionUse'] > 0 :
                                        player["health"] = player['health'] + potionStrength
                                        print(f"This potion heals for {potionStrength} health.")
                                        print(f"Your health is now {player['health']}")
                                        getchit()
                                        player['potionUse'] = 0
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
                    case 'f':
                        if player['fleeUse'] < 2:
                            print("You are exhausted and cannot flee.")
                            getchit()
                        else:
                            print("You have fled. All cards have been moved to the bottom of the deck.")
                            getchit()
                            player['fleeUse'] = 0
                            player['hasFled'] = True
                            print(deck.cards)
                            for card in room.cards:
                                deck.cards.insert(0, card)
                            room.cards.clear()
                            break
                    case 'q':
                        print("Are you sure you want to quit? y/n")
                        quitChoice = lowerisUpper(getchit())
                        if quitChoice == "Y":
                            player['quitGame'] = True
                        break
        # except:
        #     break
    mainMenu()
def drawRoom(deck, room):
    while len(room.cards) < 4:
        try:
            nextroom = deck.draw_card()
            room.cards.append(nextroom)
        except:
            print("end of deck")
            break
    print(room.cards)
    return room

# Converts inputs to uppercase, typically using this for single-character inputs.
def lowerisUpper(input):
    if input.lower() == input:
        return input.upper()
    else:
        return input
def remove_cards_from_deck(deck, remove_list):
    """
    Removes cards from deck that match strings in remove_list.
    Each string should look like 'Queen of Diamonds'.
    """
    # Keep only cards NOT in remove_list
    deck.cards = [card for card in deck.cards if card.name not in remove_list]
    return deck

def print_cards_horizontal(cards, spacing=3):
    """
    Print a list of cards side by side horizontally with conditional coloring.
    
    Args:
        cards (list): A list of Card objects with .img (ASCII art) and .suit.
        spacing (int): Number of spaces between each card.
    """
    
    # Create colored card art based on the suit
    colored_card_art = []
    for card in cards:
        lines = card.img.splitlines()
        
        # Apply red font for hearts and diamonds
        if card.suit >= 2:
            colored_lines = [Fore.RED + line for line in lines]
        # Apply white font for clubs and spades
        else:
            colored_lines = [Fore.WHITE + line for line in lines]
            
        colored_card_art.append(colored_lines)
    # Ensures all cards end up being the same height based on the highest height
    max_height = max(len(art) for art in colored_card_art)
    for art in colored_card_art:
        while len(art) < max_height:
            # Padding for shorter cards must also have a background color
            padding_line = Fore.BLACK + " " * len(art[0])
            art.append(padding_line)

    # Print row by row
    for i in range(max_height):
        # Join the corresponding line from each colored card art
        print((" " * spacing).join(art[i] for art in colored_card_art))
    print(Style.RESET_ALL)

def mainMenu():
    while True:
        clear_screen()
        print("Welcome to Scoundrel")
        print("Press 1 to Start")
        print("Press 2 for Rules/About")
        print("Press q to Quit")
        response = getchit()
        match response:
            case '1':
                game = newGame()
                playGame(game)
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
                pdfcall = getchit()
                if lowerisUpper(pdfcall) == 'H':
                    open_pdf('Scoundrel.pdf')
            case 'q':
                break
mainMenu()

