import discord
commands_list = ["hello", "play"]
class Command():

	def __init__(self, client, message, command, params):
		self.client = client
		self.message = message
		self.command = command
		self.params = params
		# self.parse_message(self):

	# def parse_message(self):
	# 	msg_string = self.message.content[1:]
 #        msg_string_list = msg_string.split()
 #        command = msg_string_list[0] # e.g. in 'play <link>', play is command
 #        self.command = command
 #        self.params = msg_string_list[1:] # list of items following play (sep by space)
 #        print("Command: " + command) # debug
 #        print("Params: " + params)

	async def execute(self):
		# commands_dict[self.command]()
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
		return



