# import discord

async def disconnect(client, message):
	for vc in client.voice_clients:
		await vc.disconnect()
		return