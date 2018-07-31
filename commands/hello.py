async def hello(client, message):
	msg = "Hello {0.author.mention}".format(message)
	await client.send_message(message.channel, msg)

