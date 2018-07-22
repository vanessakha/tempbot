import discord

class Command():
	def __init__(self, client, message, command):
		self.client = client
		self.message = message
		self.command = command

	async def execute(self):
		# commands_dict[self.command]()
		if self.command == "hello":
			await Hello.execute(self, self.client, self.message, self.command)


class Hello(Command):

	async def execute(self, client, message, command):
		msg = "Hello {0.author.mention}".format(message)
		await self.client.send_message(self.message.channel, msg)


