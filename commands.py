import discord
import youtube_dl

commands_list = ["hello", "play", "disconnect"]

class Command():

    def __init__(self, client, message, command, params, debug):
	    self.client = client
	    self.message = message
		self.command = command
		self.params = params
        self.debug = debug

    async def execute(self):
	    if self.command == "hello":
            await hello(self.client, self.message, self.debug)
        if self.command == "play":
            await play(self.client, self.message, self.params, self.debug)
		if self.command == "disconnect":
            await disconnect(self.client, self.message, self.debug)

async def hello(client, message, debug):
	msg = "Hello {0.author.mention}".format(message)
	await self.client.send_message(self.message.channel, msg)
    if debug == True:
        print("Just said hello")

async def play(client, message, params, debug):
    author = message.author
    if not(client.is_voice_connected(author.server)):
		v_channel = author.voice_channel
		v_client = await client.join_voice_channel(v_channel)
        if debug == True:
            print("Joining Voice channel")
	else:
        for vc in client.voice_clients:
            if vc.channel == author.voice_channel:
			    v_client = vc
            if debug == True:
                print("Already connected to voice")

    link = params[0]
	player = await v_client.create_ytdl_player(link, after=after_song)

    player.start()
    if debug == True:
        print("Starting song playback")

async def disconnect(client, message, debug):
    for vc in client.voice_clients:
		await vc.disconnect()
    if debug == True:
        print("Disconnected from voice")

def after_song():
    if debug == True:
        print("Finished song playback playing song")
