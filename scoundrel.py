from custom.playingcardsscoundrel import Deck
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
        'hasFled': False
    }
    
    room = deck.draw_n(4)
    
    while True:
        # try:
            enemies = 0
            for card in room.cards:
                if card.suit <= 1:
                    enemies = enemies+1
            for card in deck.cards:
                if card.suit <= 1:
                    enemies = enemies+1
            if player['hasFled'] == True:
                player['hasFled'] = False
                drawRoom(deck, room)
                player['potionUse'] = 1
            elif enemies == 0:
                print("You have survived.")
                print("Congratulations!")
                input()
                break
            else:
                if len(room.cards) == 1 and len(deck.cards) != 0:
                    drawRoom(deck, room)
                    player['potionUse'] = 1
                    if player['fleeUse'] < 2:
                        player['fleeUse'] = player['fleeUse']+1
            while enemies >= 1:
                clear_screen()
                # print("HEALTH: ",player["health"])
                # print("WEAPON: ",player["weapon"])
                # print("DURABILITY: ",player['durability'])
                # print("ENEMIES LEFT: ",enemies)
                print(f"❤ {player['health']} ❤ | ⚔ {player['weapon']}:{player['durability']} ⚔ | {enemies} enemies left")
                print(f"{'You are exhausted.' if player['fleeUse']<2 else 'You feel like you could out run them.'}")
                print_cards_horizontal(room)
                print('What would you like to do?')
                print("a - Attack | w - Wield | p - Use Potion | f - Flee")
                # try:
                choice = getchit()
                match choice:
                    case 'a':
                        print("Attacking with weapon")
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
                            print_cards_horizontal(foundEnemies['available'])
                            print("Select an enemy by typing it's value/rank or press c to cancel")
                            enemyChoice = lowerisUpper(getchit())
                            if enemyChoice == 'C':
                                break
                            selectedEnemy = foundEnemies["value"].index(enemyChoice)
                            enemyPosition = foundEnemies["room_position"][selectedEnemy]
                            enemyStrength = room.cards[enemyPosition].value
                            if enemyStrength == 1:
                                enemyStrength = 14
                            print('The enemy will do ',enemyStrength,' damage')
                            print('Use (w)eapon or (b)are hands?')
                            print('Press c to cancel this action')
                            while True:
                                weapon = getchit()
                                match weapon:
                                    case 'w':
                                        try: 
                                            while True:
                                                if player['weapon'] == 0:
                                                    print("You don't have a weapon, so you throw hands.")
                                                    weapon = int(player['weapon'])
                                                    break
                                                elif player['firststrike']:
                                                    player['durability'] = enemyStrength
                                                    player['firststrike'] = False
                                                    weapon = int(player['weapon'])
                                                    break
                                                elif enemyStrength < player['durability'] :
                                                    weapon = int(player['weapon'])
                                                    player['durability'] = enemyStrength
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
                                            break
                                        except:
                                            print("Your weapon would break from this attack.")
                                            break
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
                                        print(f"Player takes {damage} damage")
                                        break
                                    case 'c':
                                        break
                            break
                        if not foundEnemy:
                            print("No Enemies")
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
                            print_cards_horizontal(foundWeapons['available'])
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
                            print_cards_horizontal(foundPotions['available'])
                            if player['potionUse'] == 0:
                                print("You can drink another potion, but it will have no effect.")
                            print("Select a potion by typing it's rank or enter c to cancel")
                            while True:
                                potionChoice = lowerisUpper(getchit())
                                if potionChoice == 'C':
                                    break
                                selectedPotion = foundPotions["value"].index(potionChoice)
                                potionPosition = foundPotions["room_position"][selectedPotion]
                                potionStrength = room.cards[potionPosition].value
                                if potionChoice in foundPotions['value'] and player['potionUse'] > 0 :
                                    print('Potion Strength: ',potionStrength)
                                    player["health"] = player['health'] + potionStrength
                                    player['potionUse'] = 0
                                    room.remove_card(potionPosition)
                                    break
                                else:
                                    room.remove_card(potionPosition)
                                    break
                    
                        else:
                            print("No potions available")
                            
                        break
                    case 'f':
                        if player['fleeUse'] < 2:
                            print("You are exhausted and cannot flee.")
                        else:
                            print("You have fled. All cards have been moved to the bottom of the deck.")
                            player['fleeUse'] = 0
                            player['hasFled'] = True
                            print(deck.cards)
                            for card in room.cards:
                                deck.cards.insert(0, card)
                            room.cards.clear()
                            break
                # except:
                #     break            
            print("ENEMY", enemies)
        # except:
        #     print("End of Deck")
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
    Print a list of cards side by side horizontally.

    Args:
        cards (list): A list of Card objects with .img (ASCII art).
        spacing (int): Number of spaces between each card.
    """
    card_art = [card.img.splitlines() for card in cards]
    # In case the cards are different heights, normalize them
    max_height = max(len(art) for art in card_art)
    for art in card_art:
        while len(art) < max_height:
            art.append(" " * len(art[0]))  # pad shorter cards with spaces

    # Print row by row
    for i in range(max_height):
        print((" " * spacing).join(card[i] for card in card_art))

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
                print("Scoundrel is a game")
                input()
            case 'q':
                break
mainMenu()

