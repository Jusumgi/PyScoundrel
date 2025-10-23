from colorama import Fore, Style

def find_cards(suit, room):
    foundCard = False
    foundCards = {
        'available': [],
        'rank': [],
        'room_position': [],
        'value': []
    }
    # "Renders" the room in search of cards
    for index, card in enumerate(room.cards):
        if card.suit_name == suit:
            foundCard = True
            foundCards['available'].append(card)
            foundCards['rank'].append(str(card.rank)[0]) # card.rank[0] is returning the first character of ranks, like King becomes "K"
            foundCards['room_position'].append(index)
            foundCards['value'].append(card.value)
        
    return foundCard, foundCards

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
        finalprint = (" " * spacing).join(art[i] for art in colored_card_art)
        print(finalprint)
    print(Style.RESET_ALL)