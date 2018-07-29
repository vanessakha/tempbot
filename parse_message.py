def parse_message(message):
	msg_string = message.content[1:]
	msg_string_list = msg_string.split()
	command = msg_string_list[0]
	params = msg_string_list[1:]
	return command, params
