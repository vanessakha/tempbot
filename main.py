# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
from vars import token
from commands import * 
from parse_message import *
from opus_load import *

client = discord.Client()

opus_load()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        command, params = parse_message(message) # !command param1 param2
        if command in commands_list:
            new_command = Command(client, message, command, params)
            await new_command.execute()

client.run(token)
