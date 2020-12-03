import discord
#import PyNaCl
from discord.ext import commands

b = commands.Bot(command_prefix = '.')

@b.event
async def on_ready():
	print('Bot is ready.')

'''@b.event
async def on_member_join(member):
	print(f'{member} has joined a server')

@b.event
async def on_member_remove(member):
	print(f'{member} has left a server')'''

@b.command()
async def join(c):
	try:
		channel = c.author.voice.channel
		await channel.connect()
	except:
		return "already joined"

@b.command()
async def leave(c):
	try:
		await c.voice_client.disconnect()
	except:
		return "already left"


badum = discord.FFmpegPCMAudio('Sounds/badum-tss.mp3')
wow = discord.FFmpegPCMAudio('Sounds/anime-wow-sound-effect.mp3')
fbi = discord.FFmpegPCMAudio('Sounds/fbi-open-up.mp3')
illuminati = discord.FFmpegPCMAudio('Sounds/illuminati.mp3')
moment = discord.FFmpegPCMAudio('Sounds/it-was-at-this-moment.mp3')
airhorn = discord.FFmpegPCMAudio('Sounds/airhorn.mp3')
bruh = discord.FFmpegPCMAudio('Sounds/bruh.mp3')
oof = discord.FFmpegPCMAudio('Sounds/oof.mp3')
nani = discord.FFmpegPCMAudio('Sounds/nani.mp3')
sad = discord.FFmpegPCMAudio('Sounds/sad.mp3')
snoop = discord.FFmpegPCMAudio('Sounds/snoop.mp3')
why = discord.FFmpegPCMAudio('Sounds/why-are.mp3')
yeet = discord.FFmpegPCMAudio('Sounds/yeet.mp3')

@b.command(aliases=['m','random'])
async def meme(c,*,meme):
	try:
		channel = c.author.voice.channel
		ch = await channel.connect()
	except:
		print("Already in voice")

	try:
		guild = c.guild
		voice_client: discord.VoiceClient = discord.utils.get(b.voice_clients, guild=guild)

		if(meme=="badum"):
			voice_client.play(badum, after=None)

		elif(meme=="wow"):
			voice_client.play(wow, after=None)

		elif(meme=="fbi"):
			voice_client.play(fbi, after=None)

		elif(meme=="illuminati"):
			voice_client.play(illuminati, after=None)

		elif(meme=="moment"):
			voice_client.play(moment, after=None)

		elif(meme=="airhorn"):
			voice_client.play(airhorn, after=None)

		elif(meme=="bruh"):
			voice_client.play(bruh, after=None)

		elif(meme=="oof"):
			voice_client.play(oof, after=None)

		elif(meme=="nani"):
			voice_client.play(nani, after=None)

		elif(meme=="sad"):
			voice_client.play(sad, after=None)

		elif(meme=="snoop"):
			voice_client.play(snoop, after=None)

		elif(meme=="why"):
			voice_client.play(why, after=None)

		elif(meme=="yeet"):
			voice_client.play(yeet, after=None)
			
		else:
			return "Sorry Wrong command"
	except:
		return "cannot play"


b.run('NzgzMjQyNjkwNDM1MjE5NDk3.X8X5mQ.wZU_3vV2pLYogkOnuUJ5IFcUgWc')

#non admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=36781312&scope=bot

#admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=8&scope=bot