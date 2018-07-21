# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord

TOKEN = 'NDcwMjg4MzYxNDY3MjgxNDM0.DjUIUw.DCm4ogdyzGSKYb3Ctn7P9xeY5qQ'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
