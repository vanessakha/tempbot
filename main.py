# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
from vars import *
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

@client.event
async def on_member_join(member):
    
    # add welcome_channel_id to vars.py
    await client.send_message(client.get_channel(welcome_channel_id), "Welcome, " + member.mention + "!")
    private_ch = await client.start_private_message(member)
    await client.send_message(private_ch, "Welcome to temp server!")

client.run(token)
