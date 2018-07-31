import googletrans
translator = googletrans.Translator()

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