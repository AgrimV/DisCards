import os
import discord
import blackjack

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} is on!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$blackjack'):
        await blackjack.main(client, message)


client.run(os.getenv('TOKEN'))
