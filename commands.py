import discord
import youtube_dl

commands_list = ["hello", "play"]
class Command():

	def __init__(self, client, message, command, params):
		self.client = client
		self.message = message
		self.command = command
		self.params = params

	async def execute(self):
		if self.command == "hello":
			await Hello.execute(self, self.client, self.message)
		if self.command == "play":

			await Play.execute(self, self.client, self.message, self.params)

class Hello(Command):

	async def execute(self, client, message):
		msg = "Hello {0.author.mention}".format(message)
		await self.client.send_message(self.message.channel, msg)

class Play(Command):

	async def execute(self, client, message, params):
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

def after_song(): # debugging purposes
	print("Finished playing song.")
	


