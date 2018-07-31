async def purge(client, message, params):
	num_to_purge = params[0]
	if not(num_to_purge.isdigit()) or int(num_to_purge) <= 0:
		await client.send_message(message.channel, "Not a valid purge number. Please repeat the command with a positive integer.")
		return
	else:
		num_to_purge = int(num_to_purge) + 1
		await client.purge_from(message.channel, limit=num_to_purge)