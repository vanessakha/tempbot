import youtube_dl

async def play(client, message, params):
	author = message.author
	if not(client.is_voice_connected(author.server)):
		v_channel = author.voice_channel
		v_client = await client.join_voice_channel(v_channel)
	else:
		print("Already connected to voice") # d
		for vc in client.voice_clients:
			if vc.channel == author.voice_channel:
				v_client = vc

	link = params[0]
	player = await v_client.create_ytdl_player(link, after=after_song)

	try:
		player.start()
	except:
		await client.send_message("Must use a valid Youtube URL.")

	print("Playing song now") # d

def after_song(): # debugging purposes
	print("Finished playing song.") # d