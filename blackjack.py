import random
import discord
import itertools

houses = ['H', 'S', 'C', 'D']
house_emoji = {'H': ':heart:',
               'S': ':spades:',
               'C': ':clubs:',
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
              'J': ':fleur_de_lis:',
              'Q': ':trident:',
              'K': ':crown:'}
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

DECK = [''.join(card) for card in list(itertools.product(houses, faces))]

dealer_hand = []
player_hand = []


def draw_card():
    card = DECK[random.randint(0, len(DECK) - 1)]
    DECK.remove(card)
    return card


def emojify(cards):
    house = []
    face = []
    for card in cards:
        house.append(house_emoji[card[0]])
        face.append(face_emoji[card[1]])
    return house, face


def player_show():
    player_cards = emojify(player_hand)
    return '\n'.join([''.join(player_cards[0]),
                      ''.join(player_cards[1])])


def dealer_show(hidden):
    dealer_cards = emojify(dealer_hand)
    if hidden:
        return '\n'.join([f'{dealer_cards[0][0]}' + ':question:',
                          f'{dealer_cards[1][0]}' +
                          ':face_with_raised_eyebrow:'])

    else:
        return '\n'.join([''.join(dealer_cards[0]),
                          ''.join(dealer_cards[1])])


async def begin(message):
    global DECK, dealer_hand, player_hand

    DECK = [''.join(card) for card in list(itertools.product(houses, faces))]

    dealer_hand = []
    player_hand = []

    dealer_hand.append(draw_card())
    dealer_hand.append(draw_card())

    player_hand.append(draw_card())
    player_hand.append(draw_card())

    embed = discord.Embed(title='BLACKJACK', color=discord.Color.blue())
    embed.add_field(name='Dealer Hand', value=dealer_show(True), inline=True)
    embed.add_field(name='Player Hand', value=player_show(), inline=True)
    await message.channel.send(embed=embed)


async def player_draw(message):
    player_hand.append(draw_card())
    embed = discord.Embed(title='BLACKJACK', description='Player Hits',
                          color=discord.Color.blue())
    embed.add_field(name='Player', value='Card Drawn', inline=False)
    embed.add_field(name='Dealer Hand', value=dealer_show(True), inline=True)
    embed.add_field(name='Player Hand', value=player_show(), inline=True)

    await message.channel.send(embed=embed)


async def show(message):
    embed = discord.Embed(title='BLACKJACK', color=discord.Color.blue())
    embed.add_field(name='Dealer Hand', value=dealer_show(False), inline=True)
    embed.add_field(name='Player Hand', value=player_show(), inline=True)

    await message.channel.send(embed=embed)

    player_value = sum([face_value[i[1]] for i in player_hand])
    dealer_value = sum([face_value[i[1]] for i in dealer_hand])

    player_ace_count = 0
    dealer_ace_count = 0

    if player_value > 21:
        for card in player_hand:
            if 'A' in card:
                player_ace_count += 1

    if player_ace_count > 1:
        player_value -= 10 * (player_ace_count - 1)
    elif player_ace_count == 1:
        player_value -= 10

    if dealer_value > 21:
        for card in dealer_hand:
            if 'A' in card:
                dealer_ace_count += 1

    if dealer_ace_count > 1:
        dealer_value -= 10 * (dealer_ace_count - 1)
    elif dealer_ace_count == 1:
        dealer_value -= 10

    while dealer_value < 17:
        dealer_hand.append(draw_card())
        embed = discord.Embed(title='BLACKJACK', description='Dealer Hits',
                              color=discord.Color.blue())
        embed.add_field(name='Dealer Hand', value=dealer_show(False),
                        inline=True)
        embed.add_field(name='Player Hand', value=player_show(), inline=True)
        await message.channel.send(embed=embed)
        dealer_value = sum([face_value[i[1]] for i in dealer_hand])

    embed = discord.Embed(title='BLACKJACK', description='Show',
                          color=discord.Color.blue())
    embed.add_field(name='Dealer Hand', value=dealer_show(False), inline=True)
    embed.add_field(name='Player Hand', value=player_show(), inline=True)
    embed.add_field(name='|', value='|', inline=True)
    embed.add_field(name='Dealer Value', value=f'{dealer_value}', inline=True)
    embed.add_field(name='Player Value', value=f'{player_value}', inline=True)

    if player_value > 21:
        embed.add_field(name='You are BUSTED!', value=':cop::scream::spy:',
                        inline=False)
    elif player_value == 21:
        embed.add_field(name='BLACKJACK! You WIN!', value=':black_joker:',
                        inline=False)
    elif player_value == dealer_value:
        embed.add_field(name='Draw', value=':handshake:', inline=False)
    elif dealer_value > 21:
        embed.add_field(name='Dealer BUSTED!', value=':cop::unamused::spy:',
                        inline=False)
    elif player_value > dealer_value:
        embed.add_field(name='You Win!', value=':partying_face:', inline=False)
    else:
        embed.add_field(name='You Lose!', value=':tired_face:', inline=False)

    await message.channel.send(embed=embed)
