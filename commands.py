import discord
import youtube_dl
import googletrans
translator = googletrans.Translator()

commands_list = ["hello", "play", "disconnect", "purge", "translate", "poll"]

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
		if self.command == "purge":
			await purge(self.client, self.message, self.params)
		if self.command == "poll":
			await poll(self.client, self.message, self.params)

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

async def translate(client, message, params):
	src_lang = params.pop(-2) #the source language must be the second to last item
	dest_lang = params.pop(-1) #the destination language must be the last item
	to_be_translated = " ".join(params) #the text to be translated is what remains

	if src_lang not in googletrans.LANGUAGES: #ensures that src_lang is a valid source language
		await client.send_message(message.channel, "\""+src_lang+"\" is not a valid source language.")
		return
	if dest_lang not in googletrans.LANGUAGES: #ensures that dest_lang is a valid destination language
		await client.send_message(message.channel, "\""+dest_lang+"\" is not a valid destination language.")
		return

	translated_text = translator.translate(to_be_translated, src=src_lang, dest=dest_lang)

	final_msg = "`Original text: \"%s\" (source language: %s)\nTranslated text: \"%s\" (destination language: %s)`" % (to_be_translated, translated_text.src, translated_text.text, translated_text.dest)
	await client.send_message(message.channel, final_msg)
	return

async def poll(client, message, params):

	if not params:
		await client.send_message(message.channel, "Must ask a question in order to begin poll.")
		return 

	question = " ".join(params)
	await client.send_message(message.channel, "Type 'start' when you are done adding options.")
	option_num = '1'
	options_list = []

	options_count = 0
	max_options = 9
	option_letter = '1'
	option_msg = None

	while (option_msg == None or option_msg.content != "start") and max_options <= max_options:
		new_option = await client.send_message(message.channel, "Option " + option_letter + ": \n")
		option_msg = await client.wait_for_message(author=message.author)
		options_list.append(new_option.content + " " + option_msg.content)
		option_letter = chr(ord(option_letter) + 1)
		options_count += 1

	options_list.pop()
	options_count -= 1

	if options_count == 0:
		await client.send_message(message.channel, "Must specify some options to start poll.")
		return

	options_string = "\n".join(options_list)
	poll_msg = await client.send_message(message.channel, "Poll time! Here's the question:\n" + question + "\n" + options_string + "\n" + "Vote by reacting with the respective emoji!")

	emojis_str_list = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}", 
						"\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
						"\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}", 
						"\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}", 
						"\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}"]

	reactions_count = 0
	while reactions_count < options_count:
		await client.add_reaction(poll_msg, emojis_str_list[reactions_count])
		reactions_count += 1

def after_song(): # debugging purposes
	print("Finished playing song.")
