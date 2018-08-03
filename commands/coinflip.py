import random

async def coinflip(client, message):

    #random.randint(0,1) returns either 0 or 1, if it's 1 then the bot says "Heads!"...
    if random.randint(0,1): await client.send_message(message.channel, "Heads!")

    #...and if not, the bot says "Tails!"
    else: await client.send_message(message.channel, "Tails!")
