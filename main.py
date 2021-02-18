import os
import discord
import blackjack

CLIENT = discord.Client()


@CLIENT.event
async def on_ready():
    print(f'{CLIENT.user} is on!')


@CLIENT.event
async def on_message(message):
    if message.author == CLIENT.user:
        return

    if message.content.startswith('$blackjack'):
        await blackjack.main(CLIENT, message)


CLIENT.run(os.getenv('TOKEN'))
