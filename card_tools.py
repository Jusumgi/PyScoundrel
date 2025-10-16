def find_cards(suit, room):
    foundCard = False
    foundCards = {
        'available': [],
        'value': [],
        'room_position': []
    }
    # "Renders" the room in search of enemies
    for index, card in enumerate(room.cards):
        if card.suit_name == suit:
            foundCard = True
            foundCards["available"].append(card)
            foundCards["value"].append(str(card.rank)[0])
            foundCards['room_position'].append(index)
        
    return foundCard, foundCards