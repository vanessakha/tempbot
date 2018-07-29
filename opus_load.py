import discord

opus_libs = ['libopus.0.dylib', 'libopus-0.dll', 'libopus.so.0']
# must download libopus for your respective OS for bot to use voice
	# mac and windows opus libs added, but linux needs to do this step
	# either place in this directory set up path to make it recognizeable

def opus_load():
	for lib in opus_libs:
		try: 
			discord.opus.load_opus(lib)
			return
		except:
			pass