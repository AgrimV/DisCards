import os
import discord

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} is on!")


@client.event
async def on_message(message):
    global count
    if message.author == client.user:
        return

    if message.content.startswith("`yo"):
        await message.channel.send("Yo!")
        await message.channel.send(message.author)


client.run(os.getenv("TOKEN"))
