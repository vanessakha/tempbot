import discord
import youtube_dl
import googletrans

commands_list = ["hello", "play", "disconnect", "translate"]

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
		if self.command == "translate":
			await translate(self.client, self.message, self.params)

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

async def translate(client, message, params):
	params_list = params.split(" ")
	to_be_translated = params_list[0]
	for x in range(len(params_list)):
		if x != 0:
			if params_list[x][:3] == "src":
				src_lang = params_list[x][4:]
			if params_list[x][:4] == "dest":
				dest_lang = params_list[x][5:]
	if src_lang not in googletrans.LANGUAGES:
		await self.client.send_message(self.message.channel, "That is not a valid source language.")
		return
	if dest_lang not in googletrans.LANGUAGES:
		await self.client.send_message(self.message.channel, "That is not a valid destination language.")
		return
	translated_text = googletrans.translator.translate(to_be_translated, src=src_lang, dest=dest_lang)

	final_msg = "Original text: \"%s\" (source language: %s)\nTranslated text: \"%s\" (destination language: %s)" % to_be_translated, src_lang, translated_text.text, dest_lang
	await self.client.send_message(self.message.channel, final_msg)
	return

#		msg = "Hello {0.author.mention}".format(message)
#		await self.client.send_message(self.message.channel, msg)



def after_song(): # debugging purposes
	print("Finished playing song.")
