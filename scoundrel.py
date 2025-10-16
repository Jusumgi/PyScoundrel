from custom.playingcardsscoundrel import Deck
from colorama import Fore, Style
from tools import *
from card_tools import *

def newGame():
    """Generates new deck, removes cards for normal-mode"""
    freshdeck = Deck() # generate standard 52-card deck
    remove_cards_normal = ["Ace of Hearts", "Ace of Diamonds", "King of Hearts", "King of Diamonds", "Queen of Hearts", "Queen of Diamonds", "Jack of Hearts", "Jack of Diamonds"]
    deck = remove_cards_from_deck(freshdeck, remove_cards_normal)
    deck.shuffle()
    return deck

def playGame(deck):
    """ Game plays until enemies are 0 or player ends the game"""
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
            # if player has pressed q while game is in session, exit the game session.
            if player['quitGame']: 
                break

            # Enemy counter is tracked to determine when the game is over (as a win condition). Will have to change this when Scoring is implemented
            enemies = 0 

            # Check the room and if the card suit is 0 or 1 (Clubs or Spades) then add 1 to enemies counter.
            for card in room.cards: 
                if card.suit <= 1:
                    enemies = enemies+1

            # Check the deck and if the card suit is 0 or 1 (Clubs or Spades) then add 1 to enemies counter.
            for card in deck.cards: 
                if card.suit <= 1:
                    enemies = enemies+1

            # When player's health is 0 or less, ask if player wants to continue as an Undead or end the game.
            if player['health'] <= 0 and player['undead'] == False:
                print(f"Alas, you have fallen in battle.")
                print("Continue as an undead? y/n" ) 
                deathChoice = lowerisUpper(input())
                if deathChoice == 'Y':
                    player['undead'] = True
                    print("Resurrecting as an undead.")
                else:
                    break

            # This is to ensure that a full room is drawn after a Flee is used.
            if player['hasFled'] == True: 
                player['hasFled'] = False
                drawRoom(deck, room)
                player['potionUse'] = 1

            # WIN CONDITION
            elif enemies == 0: 
                if player['undead']:
                    print('With no more enemies to attack, you wander aimlessly until another scoundrel appears.')
                    input()
                    break
                print("You have survived.")
                print("Congratulations!")
                input()
                break

            # Ensures that the game continues to draw cards so long as there are cards in the "Deck"
            else:
                if len(room.cards) == 1 and len(deck.cards) != 0: 
                    drawRoom(deck, room)
                    player['potionUse'] = 1
                    if player['fleeUse'] < 2:
                        player['fleeUse'] = player['fleeUse']+1 # Flee cooldown

            # So long as there are enemies, we will continue the game.
            while enemies >= 1:
                clear_screen()
                print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                print(f"{'You are exhausted.' if player['fleeUse']<2 else 'You feel like you could out run them.'}")
                print_cards_horizontal(room)
                print('What would you like to do?')
                print("a - Attack | w - Wield | p - Use Potion | f - Flee | q - Quit")
                choice = getchit()
                match choice:

                    # Attack
                    case 'a':
                        # foundEnemies = {
                        #     'available': [],
                        #     'value': [],
                        #     'suit': [],
                        #     'room_position': []
                        # }
                        # # "Renders" the room in search of enemies
                        # for index, card in enumerate(room.cards):
                        #     if card.suit_name == 'Clubs' or card.suit_name == 'Spades':
                        #         foundEnemy = True
                        #         foundEnemies["available"].append(card)
                        #         foundEnemies["value"].append(str(card.rank)[0])
                        #         foundEnemies['suit'].append(str(card.suit_name)[0])
                        #         foundEnemies['room_position'].append(index)
                        findClubs = find_cards("Clubs", room)
                        findSpades = find_cards("Spades", room)
                        foundEnemies = {key: findClubs[1][key] + findSpades[1][key] for key in findClubs[1]}
                        # Enemy must be present for the condition to pass.
                        if findClubs[0] or findSpades[0]:
                            clear_screen()
                            print(f"{Fore.RED}❤ {player['health']}{Fore.RED}❤ {Style.RESET_ALL}| {Fore.YELLOW}⚔ {player['weapon']}{Style.RESET_ALL}:{Fore.CYAN}{player['durability']} ⚔ {Style.RESET_ALL}| {enemies} enemies left")
                            print("Attacking")
                            print_cards_horizontal(foundEnemies['available'])
                            print(Style.RESET_ALL)
                            print("Select an enemy by typing it's value/rank or press c to cancel")

                            # Input will accept c for cancel, and the rank of the card to target. If the rank isn't present, it is an invalid selection.
                            while True:
                                try:
                                    enemyChoice = lowerisUpper(getchit())
                                    if enemyChoice == 'C':
                                        break
                                    selectedEnemy = foundEnemies["value"].index(enemyChoice)
                                    enemyPosition = foundEnemies["room_position"][selectedEnemy]
                                    enemyStrength = room.cards[enemyPosition].value

                                    # Aces Low into Aces High
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

                            # Cancel case
                            if enemyChoice == 'C':
                                break

                            # If a valid rank is selected and the prompt wasn't cancels, we continue to the next loop
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

                                                # With first strike, a weapon can strike any enemy without restriction.
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
                                            # If enemy is an Ace, damage needs to be 14.
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
                        else:
                            print("No Enemies")
                            getchit()
                        break   

                    # Wield Weapon         
                    case 'w':
                        # foundWeapon = False
                        # foundWeapons = {
                        #     'available': [],
                        #     'value': [],
                        #     'room_position': []
                        # }
                        # for index, card in enumerate(room.cards):
                        #     if card.suit_name == 'Diamonds':
                        #         foundWeapon = True
                        #         foundWeapons["available"].append(card)
                        #         foundWeapons["value"].append(str(card.rank))
                        #         foundWeapons['room_position'].append(index)
                        findDiamonds = find_cards("Diamonds", room)
                        foundWeapons = findDiamonds[1]
                        if findDiamonds[0]:
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

                    # Use Potion
                    case 'p':
                        # foundPotion = False
                        # foundPotions = {
                        #     'available': [],
                        #     'value': [],
                        #     'room_position': []
                        # }
                        
                        # for index, card in enumerate(room.cards):
                        #     if card.suit_name == 'Hearts':
                        #         foundPotion = True
                        #         foundPotions["available"].append(card)
                        #         foundPotions["value"].append(str(card.rank))
                        #         foundPotions['room_position'].append(index)
                        findHearts = find_cards("Hearts", room)
                        foundPotions = findHearts[1]
                        if findHearts[0]:
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

                    # Flee Room
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

                    # Quit Game
                    case 'q':
                        print("Are you sure you want to quit? y/n")
                        quitChoice = lowerisUpper(getchit())
                        if quitChoice == "Y":
                            player['quitGame'] = True
                        break


def drawRoom(deck, room):
    """
    Draws cards from Deck and appends the drawn cards to Room list. 
    """

    while len(room.cards) < 4:
        try:
            nextroom = deck.draw_card()
            room.cards.append(nextroom)
        except:
            print("end of deck")
            break
    print(room.cards)
    return room

def remove_cards_from_deck(deck, remove_list):
    """
    Removes cards from deck that match strings in remove_list.
    Each string should look like 'Queen of Diamonds'.
    """
    # Keep only cards NOT in remove_list, using list comprehension. The [card ...] is added to a new list if card.name condition returns true.
    # After list comprehension, the new list overwrites deck by returning this new deck with cards removed.
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

        # Takes a multi-line string (card.img) and split it in to a LIST of individual lines so that they may be colored and re-joined to print horizontally.
        # This is so we work with strings rather than working directly with the card object.
        lines = card.img.splitlines() 
        
        # Apply red font for hearts and diamonds
        if card.suit >= 2:
            colored_lines = [Fore.RED + line for line in lines]
        # Apply white font for clubs and spades
        else:
            colored_lines = [Fore.WHITE + line for line in lines]
        # Becomes a list of lists, each member of the list is a card deconstructed into it's colored lines.
        colored_card_art.append(colored_lines)

    # Print each card's lines by their index, by joining them. Join all card's 0 line, then 1 line, etc.
    # The playingcards module by default always prints 7 lines to create a card.
    for i in range(7):
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

