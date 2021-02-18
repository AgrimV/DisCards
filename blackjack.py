import random
import itertools

houses = ['H', 'S', 'C', 'D']
house_emoji = {'H': ':heart:',
               'S': ':spades:',
               'C': ':four_leaf_clover:',
               'D': ':diamonds:'}

faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
face_emoji = {'A': ':a:',
              '2': ':two:',
              '3': ':three:',
              '4': ':four:',
              '5': ':five:',
              '6': ':six:',
              '7': ':seven:',
              '8': ':eight:',
              '9': ':nine:',
              'T': ':keycap_ten:',
              'J': ':jack_o_lantern:',
              'Q': ':female_sign:',
              'K': ':male_sign:'}

deck = [''.join(card) for card in list(itertools.product(houses, faces))]

dealer_hand = []
player_hand = []


def draw_card():
    card = deck[random.randint(0, len(deck) - 1)]
    deck.remove(card)
    return card


def emojify(cards):
    house = []
    face = []
    for card in cards:
        house.append(house_emoji[card[0]])
        face.append(face_emoji[card[1]])
    return house, face


async def main(client, message):
    dealer_hand.append(draw_card())
    dealer_hand.append(draw_card())
    await message.channel.send('Dealer Hand :\n')
    shown_card = emojify(dealer_hand)
    await message.channel.send('\n'.join([f'{shown_card[0][0]}:question:',
                               f'{shown_card[1][0]}:face_with_raised_eyebrow:'
                                          ]))

    player_hand.append(draw_card())
    player_hand.append(draw_card())

    await message.channel.send('Player Hand :\n')
    player_cards = emojify(player_hand)
    await message.channel.send('\n'.join([''.join(player_cards[0]),
                                          ''.join(player_cards[1])]))
