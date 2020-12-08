import discord,random, os
from discord.ext import commands,tasks
import asyncio, datetime, pytz
from Database import *

l = ["badum","wow","fbi","illuminati","moment","airhorn","bruh","oof","nani","sad","snoop","why","yeet"]
b = commands.Bot(command_prefix = os.getenv('PREFIX'))

b.remove_command('help')

'''
@b.event
async def on_member_join(member):
	print(f'{member} has joined a server')

@b.event
async def on_member_remove(member):
	print(f'{member} has left a server')'''


@b.event
async def on_ready():
	print('Bot is up and running sir.')
	find.start()
	for ser in b.guilds: 
		for channel in ser.text_channels:
			if channel.permissions_for(ser.me).send_messages:
				#await channel.send("The bot will be offline for updates")
				#await channel.send("The bot is back online")
				break


@tasks.loop(seconds=3)
async def find():
	#with contextlib.suppress(Exception):
	try:
		#print("haii")
		for ids in b.guilds:
			connect(ids.id)
			sh=search()
			if sh:
				for ch in ids.text_channels:
					if ch.permissions_for(ids.me).send_messages:
						for i in range(len(sh)):
							embed = discord.Embed(
							colour = discord.Colour.orange()
							)
							embed.add_field(name='Reminder!!!',value=sh[i][2],inline=False)
							await ch.send(embed=embed)
							await ch.send(sh[i][1])
							remove(sh[i][0])
						break
			close()		
	except:
		pass

@b.command()
async def join(c):
	try:
		channel = c.author.voice.channel
		await channel.connect()
	except:
		pass


@b.command()
async def leave(c):
	try:
		await c.voice_client.disconnect()
	except:
		pass


@b.command(aliases=['m','random'])
async def meme(c,*,meme):
	try:
		channel = c.author.voice.channel
		ch = await channel.connect()
	except:	
		pass
	
	try:
		guild = c.guild
		voice_client: discord.VoiceClient = discord.utils.get(b.voice_clients, guild=guild)
		
		if(meme=="random"):
			meme=random.choice(l)

		if(meme=="badum"):
			badum = discord.FFmpegPCMAudio('Sounds/badum-tss.mp3')
			voice_client.play(badum, after=None)

		elif(meme=="wow"):
			wow = discord.FFmpegPCMAudio('Sounds/anime-wow-sound-effect.mp3')
			voice_client.play(wow, after=None)

		elif(meme=="fbi"):
			fbi = discord.FFmpegPCMAudio('Sounds/fbi-open-up.mp3')
			voice_client.play(fbi, after=None)

		elif(meme=="illuminati"):
			illuminati = discord.FFmpegPCMAudio('Sounds/illuminati.mp3')
			voice_client.play(illuminati, after=None)

		elif(meme=="moment"):
			moment = discord.FFmpegPCMAudio('Sounds/it-was-at-this-moment.mp3')
			voice_client.play(moment, after=None)

		elif(meme=="airhorn"):
			airhorn = discord.FFmpegPCMAudio('Sounds/airhorn.mp3')
			voice_client.play(airhorn, after=None)

		elif(meme=="bruh"):
			bruh = discord.FFmpegPCMAudio('Sounds/bruh.mp3')
			voice_client.play(bruh, after=None)

		elif(meme=="oof"):
			oof = discord.FFmpegPCMAudio('Sounds/oof.mp3')
			voice_client.play(oof, after=None)

		elif(meme=="nani"):
			nani = discord.FFmpegPCMAudio('Sounds/nani.mp3')
			voice_client.play(nani, after=None)

		elif(meme=="sad"):
			sad = discord.FFmpegPCMAudio('Sounds/sad.mp3')
			voice_client.play(sad, after=None)

		elif(meme=="snoop"):
			snoop = discord.FFmpegPCMAudio('Sounds/snoop.mp3')
			voice_client.play(snoop, after=None)

		elif(meme=="why"):
			why = discord.FFmpegPCMAudio('Sounds/why-are.mp3')
			voice_client.play(why, after=None)

		elif(meme=="yeet"):
			yeet = discord.FFmpegPCMAudio('Sounds/yeet.mp3')
			voice_client.play(yeet, after=None)
		
		#malay meme
		elif(meme=="2kali"):
			kali = discord.FFmpegPCMAudio('Sounds/Malay/2kali.mp3')
			voice_client.play(kali, after=None)

		elif(meme=="betul"):
			kali = discord.FFmpegPCMAudio('Sounds/Malay/betulahtu.mp3')
			voice_client.play(kali, after=None)

		else:
			mh = discord.Embed(
				colour = discord.Colour.orange()
			)

			mh.set_author(name='.meme <name>  OR  .m <name>')
			mh.add_field(name='Where <name> is:',value='badum\n\twow\n\tfbi\n\tilluminati\n\tmoment\n\tairhorn\n\tbruh\n\toof\n\tnani\n\tsad\n\tsnoop\n\twhy\n\tyeet',inline=False)
			await c.send(embed=mh)
	except:
		pass


@b.command(pass_c=True)
async def help(c):
	author = c.message.author
	embed = discord.Embed(
		colour = discord.Colour.orange()
	)

	embed.set_author(name='Help')
	embed.add_field(name='.join',value='Join voice channel',inline=False)
	embed.add_field(name='.leave',value='Leave voice channel',inline=False)
	embed.add_field(name='.meme help',value='See memes commanands',inline=False)
	embed.add_field(name='.meme random',value='Play random memes',inline=False)
	embed.add_field(name='.remind help',value='See reminder commands',inline=False)

	await c.send(embed=embed)


@b.command(aliases=['r','reminder'])
async def remind(c,*,remind):
	d,t=[],[]
	if(remind=="help"):
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Reminder')
		embed.add_field(name='.remind <data>  OR  .r <data>',value='Used to store reminders and it will notify the person tagged 10 minutes before',inline=False)
		embed.add_field(name='Where <data> is:',value='<Mentions>, <Messages>, <Day/Month/Year>, <Time in 24 hours>',inline=False)
		await c.send(embed=embed)
		return

	try:
		r = [x.strip() for x in remind.split(',')]
		if(len(r) == 4):
			#global d,t,dt
			d = list(map(int, r[2].split('/')))
			t=[r[3][0:2],r[3][2:4]]
			t = list(map(int, t))
			dt = datetime.datetime(year=int(d[2]),month=int(d[1]),day=int(d[0]),hour=int(t[0]),minute=int(t[1]),tzinfo=pytz.timezone("Asia/Kuala_Lumpur"))
			if(len(d)==3 and len(t)==2 and dt>datetime.datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))):
				connect(c.guild.id)
				insert(r[0],r[1],dt.strftime("%c"))
			else:
				embed = discord.Embed(
					colour = discord.Colour.orange()
				)
				embed.set_author(name='Wrong Date or Time')
				embed.add_field(name='Please enter Date or Time that is in the future',value='Seriously? Are you time travelling?\n\nDo ".remind help." for reminder help',inline=False)
				await c.send(embed=embed)
	except:
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Wrong Format')
		embed.add_field(name='Please enter according to:',value='<Mentions>, <Messages>, <Day/Month/Year>, <Time in 24 hours>\n\nDo ".remind help." for reminnder help',inline=False)
		await c.send(embed=embed)

@b.command()
async def who(c,*,ext):
	if "handsome" in ext or "hensem" in ext:
		if c.author.id == os.getenv('HAPPY'):
			await c.send('You are the most handsome person in this server, Shameer')
		else:
			await c.send('I do not want to answer that')


b.run(os.getenv('TOKEN'))


#non admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=36781312&scope=bot

#admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=8&scope=bot
