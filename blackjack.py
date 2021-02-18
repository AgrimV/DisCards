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
face_value = {'A': 11,
              '2': 2,
              '3': 3,
              '4': 4,
              '5': 5,
              '6': 6,
              '7': 7,
              '8': 8,
              '9': 9,
              'T': 10,
              'J': 10,
              'Q': 10,
              'K': 10}

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
    dealer_cards = emojify(dealer_hand)

    player_hand.append(draw_card())
    player_hand.append(draw_card())

    async def display():
        player_cards = emojify(player_hand)
        await message.channel.send('Dealer Hand :\n')
        await message.channel.send('\n'.join([f'{dealer_cards[0][0]}' +
                                              ':question:',
                                              f'{dealer_cards[1][0]}' +
                                              ':face_with_raised_eyebrow:']))

        await message.channel.send('Player Hand :\n')
        await message.channel.send('\n'.join([''.join(player_cards[0]),
                                              ''.join(player_cards[1])]))

    async def show():
        player_cards = emojify(player_hand)

        await message.channel.send('Dealer Hand :\n')
        await message.channel.send('\n'.join([''.join(dealer_cards[0]),
                                              ''.join(dealer_cards[1])]))

        await message.channel.send('Player Hand :\n')
        await message.channel.send('\n'.join([''.join(player_cards[0]),
                                              ''.join(player_cards[1])]))

        player_value = sum([face_value[i[1]] for i in player_hand])
        dealer_value = sum([face_value[i[1]] for i in dealer_hand])

        await message.channel.send(f'\tDealer Hand: {dealer_value}')
        await message.channel.send(f'\tPlayer Hand : {player_value}')

        if player_value > 21:
            await message.channel.send('You are B-U-S-T-E-D!')
        elif player_value == 21:
            await message.channel.send('BLACKJACK 21! You WIN!!!')
        elif dealer_value > 21:
            await message.channel.send('Dealer BUSTED!')
        elif player_value > dealer_value:
            await message.channel.send('You Win!')
        else:
            await message.channel.send('You Lose!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hit'):
            player_hand.append(draw_card())
            await message.channel.send('Card Drawn')
            await display()

        if message.content.startswith('$stay'):
            await show()

    await display()


# dealer_hand.append(draw_card())
# dealer_hand.append(draw_card())
# player_hand.append(draw_card())
# player_hand.append(draw_card())
# print([face_value[i[1]] for i in player_hand])
# print(face_value[player_hand[0][1]], player_hand)
