import discord
import asyncio
import var

emojis_str_list = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
					"\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
					"\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}",
					"\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}", "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}",
					"\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}"]

async def get_question(client, message, params):
	
	if not params:
		await client.send_message(message.channel, "Must ask a question in order to begin poll.")
		var.is_polling = False
		return

	question = " ".join(params)

	return question

async def check_for_another_poll_request(client, message, msg_content):
	if msg_content == "!poll":
		await client.send_message(message.channel, "Please finish your current poll first or type 'end' in order to end the current poll.")
		return True
	return False

async def get_poll_time(client, message):
	
	poll_time = ""
	times_asked = 0
	max_poll_time = 30
	while not(poll_time.isdigit()):
		await client.send_message(message.channel, "Duration of poll in minutes: ")
		if times_asked >= 1:
			await client.send_message(message.channel, "Invalid poll duration. Please try again, or type 'end' to cancel poll.")
		poll_time_msg = await client.wait_for_message(author=message.author, channel=message.channel)
		poll_time = poll_time_msg.content
		if await check_for_another_poll_request(client, message, poll_time):
			continue
		if poll_time == "end":
			await client.send_message(message.channel, "Ending poll.")
			var.is_polling = False
			return
		if poll_time.isdigit() and int(poll_time) > max_poll_time:
			await client.send_message(message.channel, "Invalid poll duration. Please keep poll duration to a maximum of " + str(max_poll_time) + " minutes. Please try again, or type 'end' to cancel poll.")
			continue
		times_asked += 1

	poll_time = int(poll_time) * 60 # convert to seconds

	return poll_time

async def get_poll_options(client, message):
	
	await client.send_message(message.channel, "Type 'start' when you are done adding options or 'end' if you would like to end the poll.")

	option_num = '1'
	options_list = []

	options_count = 0
	max_options = 9
	option_msg = None

	while (option_msg == None or option_msg.content != "start") and options_count <= max_options:
		new_option = await client.send_message(message.channel, "Option " + option_num + ": \n")
		option_msg = await client.wait_for_message(author=message.author, channel=message.channel)
		if option_msg.content == "start" and options_count == 0:
			await client.send_message(message.channel, "Must specify some options to start poll. Please try again or type 'end' if you would like to end the poll.")
			option_msg = None
			continue
		elif option_msg.content == "end":
			await client.send_message(message.channel, "Ending poll.")
			var.is_polling = False
			return
		elif await check_for_another_poll_request(client, message, option_msg.content):
			continue
		options_list.append(new_option.content + " " + option_msg.content)
		option_num = chr(ord(option_num) + 1)
		options_count += 1

	options_list.pop()
	options_count -= 1

	options_string = "\n".join(options_list)

	return options_list, options_string

async def give_poll(client, message, question, num_options, options_string):
	
	poll_msg = await client.send_message(message.channel, "Poll time! Here's the question:\n" + question + "\n`" + options_string + "`\n" + "Vote by reacting with the respective emoji!")

	reactions_count = 0
	while reactions_count < num_options:
		await client.add_reaction(poll_msg, emojis_str_list[reactions_count])
		reactions_count += 1
	print("reactions count is " + str(reactions_count)) # d

	return poll_msg

async def count_reactions(client, message, reactions_count, cached_poll_msg):

	total_reactions = 0
	max_reactions = 0
	max_reactions_option_indices = []
	reaction_index = 0
	reaction_num = 1
	reactions_per_option = []

	for reaction in cached_poll_msg.reactions:
		print("reaction count is " + str(reaction.count)) # d
		print("The reaction_num is" + str(reaction_num)) # d
		if reaction_num > reactions_count:
			break
		option_reactions_count = reaction.count - 1 # exclude the initial reaction
		print("option_reactions_count is" + str(option_reactions_count)) # d
		if option_reactions_count > max_reactions:
			max_reactions_option_indices = []
			max_reactions_option_indices.append(reaction_index)
			max_reactions = option_reactions_count
		elif option_reactions_count == max_reactions:
			max_reactions_option_indices.append(reaction_index)
		reactions_per_option.append(option_reactions_count)
		total_reactions += option_reactions_count
		print("total_reactions is " + str(total_reactions)) # d
		reaction_num += 1
		reaction_index += 1

	print("max_reactions_option_indices: ") # d
	print(max_reactions_option_indices) # d
	if total_reactions == 0:
		await client.send_message(message.channel, "There were no votes, closing poll.")
		var.is_polling = False
		return

	print(reactions_per_option) # d
	return total_reactions, reactions_per_option, max_reactions_option_indices

def calculate_percentages(client, message, total_reactions, reactions_per_option):
	reaction_percentages = []
	for r_p_m in reactions_per_option:
		reaction_percentage = (r_p_m / total_reactions) * 100
		reaction_percentage = round(reaction_percentage, 2)
		reaction_percentages.append(reaction_percentage)

	print(reaction_percentages) # d
	return reaction_percentages

async def give_results(client, message, options_list, max_reactions_option_indices, reaction_percentages):
	
	results_list = []
	i = 0
	for option in options_list:
		results_list.append(option + " received " + str(reaction_percentages[i]) + "% of the votes.")
		i += 1

	results_str = "The poll has ended! Here are the results:\n"
	results_str = results_str + "\n".join(results_list)
	if len(max_reactions_option_indices) == 1:
		results_str = results_str + "\nThe winner is \n" + options_list[max_reactions_option_indices[0]]
	if len(max_reactions_option_indices) > 1:
		tied_list = []
		for index in max_reactions_option_indices:
			tied_list.append(options_list[index])
		tied_str = "\n".join(tied_list)
		results_str = results_str + "\nThere is a tie between the following options: \n" + tied_str
	await client.send_message(message.channel, results_str)

async def poll(client, message, params):

	poll_owner = var.current_poll_owner
	if var.is_polling:
		if poll_owner != message.author: #makes sure a poll is not already running
			await client.send_message(message.channel, "A poll is currently running. Please wait until the poll by" + poll_owner.name + "has concluded to start another one.")
		return

	var.is_polling = True
	var.current_poll_owner = message.author

	question = await get_question(client, message, params)

	if not question:
		return

	poll_time = await get_poll_time(client, message)
	if not poll_time: 
		return

	options_list, options_string = await get_poll_options(client, message) or (None, None)
	if not options_list:
		return

	poll_msg = await give_poll(client, message, question, len(options_list), options_string)

	await client.send_message(message.channel, "Polling has begun. To end poll, owner must type '!endpoll'")

	await asyncio.sleep(poll_time)

	if not(var.is_polling):
		return
	
	cached_poll_msg = discord.utils.get(client.messages, id=poll_msg.id)

	total_reactions, reactions_per_option, max_reactions_option_indices = await count_reactions(client, message, len(options_list), cached_poll_msg) or (None, None, None)
	if not total_reactions:
		return
	
	reaction_percentages = calculate_percentages(client, message, total_reactions, reactions_per_option)

	await give_results(client, message, options_list, max_reactions_option_indices, reaction_percentages)

	var.is_polling = False

async def endpoll(client, message):
	global sleep_event
	if var.is_polling == True and var.current_poll_owner == message.author:
		if sleep_event == None: 
			await client.send_message(message.channel, "Please wait until poll beginning has been announced.")
			return
		await client.loop.call_soon_threadsafe(sleep_event.cancel)
		var.is_polling = False
		await client.send_message(message.channel, "Ending poll.")


