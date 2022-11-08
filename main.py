import os
import discord
import blackjack

CLIENT = discord.Client()


@CLIENT.event
async def on_ready():
    print(f'{CLIENT.user} is on!')


@CLIENT.event
async def on_message(message):
    if message.content.startswith('$blackjack'):
        await blackjack.begin(message)

    if message.content.startswith('$hit'):
        await blackjack.player_draw(message)

    if message.content.startswith('$stand'):
        await blackjack.show(message)


CLIENT.run(os.getenv('TOKEN'))
