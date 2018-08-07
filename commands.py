import discord
import sys
sys.path.insert(0, './commands')
from hello import *
from play import *
from disconnect import *
from translate import *
from purge import *
from poll import *

commands_list = ["hello", "play", "disconnect", "purge", "translate", "poll", "coinflip"]

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
		if self.command == "coinflip":
			await coinflip(self.client, self.message)
