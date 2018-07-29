import discord
import youtube_dl

commands_list = ["hello", "play", "disconnect", "purge"]

class Command():

	def __init__(self, client, message, command, params):
		self.client = client
		self.message = message
		self.command = command
		self.params = params

	async def execute(self):
		if self.command == "hello":
			await hello(self.client, self.message)
		if self.command == "play":
			await play(self.client, self.message, self.params)
		if self.command == "disconnect":
			await disconnect(self.client, self.message)
		if self.command == "purge":
			await purge(self.client, self.message, self.params)

async def hello(client, message):
	msg = "Hello {0.author.mention}".format(message)
	await self.client.send_message(self.message.channel, msg)

async def play(client, message, params):
	author = message.author
	if not(client.is_voice_connected(author.server)):
		v_channel = author.voice_channel
		v_client = await client.join_voice_channel(v_channel)
	else: 
		print("Already connected to voice")
		for vc in client.voice_clients:
			if vc.channel == author.voice_channel:
				v_client = vc
	
	link = params[0]
	player = await v_client.create_ytdl_player(link, after=after_song)

	player.start()
	print("Playing song now")

async def disconnect(client, message):
	for vc in client.voice_clients:
		await vc.disconnect()

async def purge(client, message, params):
	num_to_purge = params[0]
	if not(num_to_purge.isdigit()) or int(num_to_purge) <= 0:
		await client.send_message(message.channel, "Not a valid purge number. Please repeat the command with a positive integer.")
		return
	else:
		num_to_purge = int(num_to_purge) + 1
		await client.purge_from(message.channel, limit=num_to_purge)

def after_song(): # debugging purposes
	print("Finished playing song.")
	


