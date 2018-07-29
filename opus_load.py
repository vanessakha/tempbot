import discord
import platform

opus_libs = ['libopus-0.dll', 'libopus.0.dylib', 'libopus.so.0', 'libopus-0.x64.dll']
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

"""
def opus_load():
	operating_system = platform.system()
	if operating_system == "Windows": #Windows
		discord.opus.load_opus("libopus-0.dll")
	if operating_system == "Darwin": #Mac
		discord.opus.load_opus("libopus.0.dylib")
	if operating_system == "Linux": #linux
		discord.opus.load_opus("libopus.so.0")
"""
