from custom.playingcardsscoundrel import Deck
from tools import *
from colorama import Back
def newGame():
    # Generates new deck, removes cards for normal-mode
    freshdeck = Deck() # generate standard 52-card deck
    remove_cards_normal = ["Ace of Hearts", "Ace of Diamonds", "King of Hearts", "King of Diamonds", "Queen of Hearts", "Queen of Diamonds", "Jack of Hearts", "Jack of Diamonds"]
    deck = remove_cards_from_deck(freshdeck, remove_cards_normal)
    # print(deck)
    deck.shuffle()
    return deck

def playGame(deck):
    player = {
        'health': 20,
        'weapon': 0,
        'firststrike': False,
        'durability': 14,
        'potionUse': 1,
        'fleeUse': 1
    }
    room = deck.draw_n(4)
    
    while True:
        # try:
            while len(room.cards) > 1:
                print_cards_horizontal(room)
                print('What would you like to do?')
                print("HEALTH: ",player["health"])
                print("WEAPON: ",player["weapon"])
                print("a - Attack | w - Wield | p - Use Potion | f - Flee")
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
                            print("Select an enemy by typing it's rank followed by it's suit #S or #C")
                            print(player)
                            enemyChoice = input()
                            enemyRank = str(enemyChoice)[0]
                            enemySuit = str(enemyChoice)[1]
                            if enemyRank in foundEnemies['value'] and enemySuit in foundEnemies["suit"]:
                                print('enemyRank',enemyRank)
                                print('enemySuit',enemySuit)
                                selectedEnemy = foundEnemies["value"].index(enemyRank)
                                enemyPosition = foundEnemies["room_position"][selectedEnemy]
                                enemyStrength = room.cards[enemyPosition].value
                                if enemyStrength == 1:
                                    enemyStrength = 14
                                print('Use (w)eapon or (b)are hands?')
                                print('Press c to cancel this action')
                                while True:
                                    weapon = input()
                                    match weapon:
                                        case 'w':
                                            try: 
                                                while True:
                                                    if player['weapon'] == 0:
                                                        print("You don't have a weapon, so you throw hands.")
                                                        weapon = player['weapon']
                                                        break
                                                    if player['firststrike']:
                                                        player['durability'] = enemyStrength
                                                        print("FS DURABILITY ", player['durability'])
                                                        player['firststrike'] = False
                                                        weapon = player['weapon']
                                                        break
                                                    print("DURABILITY ", player['durability'])
                                                    if enemyStrength < player['durability'] :
                                                        weapon = player['weapon']
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
                                    
                        if not foundEnemy:
                            print("No Enemies")
                    case 'w':
                        # print(findCards('Weapon', room))
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
                                foundWeapons["value"].append(card.rank)
                                foundWeapons['room_position'].append(index)
                        if foundWeapon:
                            print_cards_horizontal(foundWeapons['available'])
                            print("Select a weapon by typing it's rank")
                            while True:
                                weaponChoice = int(input())
                                print(type(weaponChoice))
                                if isinstance(weaponChoice, int):
                                    if weaponChoice in foundWeapons['value']:
                                        print('passed')
                                        selectedWeapon = foundWeapons["value"].index(weaponChoice)
                                        player["weapon"] = weaponChoice
                                        player["durability"] = 14
                                        player['firststrike'] = True
                                        room.remove_card(foundWeapons["room_position"][selectedWeapon])
                                        break
                                else:
                                    print('Please type a number (range 2-10)')
                        if not foundWeapon:
                            print("No weapons available")

            nextroom = deck.draw_n(3)
            for card in nextroom.cards:
                room.cards.append(card)
            input()
        # except:
        #     print("End of Deck")
        #     break

# def findCards(option, room):
#     foundCard = False
#     isEnemy = False
#     foundCards = {
#     'available': [],
#     'value': [],
#     'room_position': [],
#     'cardsuit': None,
#     'cardtype': None
#     }
#     match option:
#         case 'Weapon':
#             foundCards['cardsuit'] = 'Diamonds'
#             foundCards['cardtype'] = 'weapon'
#         case 'Attack':
#             foundCards['cardtype'] = 'enemy'
#         case 'Potion':
#             foundCards['cardsuit'] = 'Hearts'
#             foundCards['cardtype'] = 'potion'
#     for index, card in enumerate(room.cards):
#             if card.suit <= 1:
#                 isEnemy = True
#             if card.suit_name == foundCards['cardsuit'] or isEnemy:
#                     foundCard = True
#                     foundCards["available"].append(card)
#                     foundCards["value"].append(card.rank)
#                     foundCards['room_position'].append(index)
#     return foundCard, foundCards
            # if foundCard:
            #     print_cards_horizontal(foundCards['available'])
            #     print(f"Select a weapon by typing it's rank")
            #     while True:
            #         weaponChoice = int(input())
            #         if isinstance(weaponChoice, int):
            #             if weaponChoice in foundCards['value']:
            #                 print('passed')
            #                 selectedWeapon = foundCards["value"].index(weaponChoice)
            #                 player["weapon"] = weaponChoice
            #                 room.remove_card(foundCards["room_position"][selectedWeapon])
            #                 break
            #         else:
            #             print('Please type a number (range 2-10)')
            # if not foundCard:
            #     print("No weapons available")

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

# print_cards_horizontal(room, 4)

def mainMenu():
    while True:
        # clear_screen()
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

