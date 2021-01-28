import discord,random, os
from discord.ext import commands,tasks
import asyncio, datetime, pytz
from Database import *
from twilio.rest import Client

from quoters import Quote #tak bole search tapi anime
from quote.quote import quote as qu #bole search
#import quote as qu

account_sid = os.getenv('SID')
#os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.getenv('TWILIO')
#os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

files = [os.path.splitext(filename)[0] for filename in os.listdir('Sounds/English')]
filemalay = [os.path.splitext(filename)[0] for filename in os.listdir('Sounds/Malay')]
#l = ["badum","wow","fbi","illuminati","moment","airhorn","bruh","oof","nani","sad","snoop","why","yeet","knock"]

prf = os.getenv('PREFIX')
b = commands.Bot(command_prefix = prf)

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
	try:
		act = os.getenv('ACT')
		sta = os.getenv('STA')

		if act == 'PLAY':
			await b.change_presence(activity=discord.Game(name=sta))
		elif act == 'STREAM':
			await b.change_presence(activity=discord.Streaming(name=sta, url=os.getenv('URL')))
		elif act == 'LISTEN':
			await b.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=sta))
		elif act == 'WATCH':
			await b.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=sta))
	except:
		print("status error")
		pass
	
	for ser in b.guilds:
		'''try:
			print(ser)
		except:
			pass'''
		for channel in ser.text_channels:
			if channel.permissions_for(ser.me).send_messages:
				#await channel.send("The bot will be offline for updates")
				#await channel.send("The bot is back online")
				#await channel.send("Try the new <.remind> feature. Do <.remind help> for help. Note that this is still in Beta Testing")
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
		
		if meme=="random":
			meme=random.choice(files)
			au = discord.FFmpegPCMAudio('Sounds/English/'+meme+'.mp3')
			voice_client.play(au, after=None)

		elif meme in files:
			au = discord.FFmpegPCMAudio('Sounds/English/'+meme+'.mp3')
			voice_client.play(au, after=None)

		elif meme in filemalay:
			au = discord.FFmpegPCMAudio('Sounds/Malay/'+meme+'.mp3')
			voice_client.play(au, after=None)

		else:
			mh = discord.Embed(
				colour = discord.Colour.orange()
			)

			mh.set_author(name=prf + 'meme <name>  OR  '+prf+'m <name>')
			mh.add_field(name='Where <name> is:',value='\n'.join(files),inline=False)
			#badum\n\twow\n\tfbi\n\tilluminati\n\tmoment\n\tairhorn\n\tbruh\n\toof\n\tnani\n\tsad\n\tsnoop\n\twhy\n\tyeet\n\tknock
			mh.add_field(name='Malay memes:',value='\n'.join(filemalay),inline=False)
			#'Malay memes:',value='2kali\n\tbetul\n\takal\n\tkur\n\tjawab\n\ttaktau'
			await c.send(embed=mh)
	except:
		pass


@b.command(pass_c=True)
async def help(c):
	try:
		author = c.message.author
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)

		embed.set_author(name='Help')
		embed.add_field(name=prf+'join',value='Join Voice Channel',inline=False)
		embed.add_field(name=prf+'leave',value='Leave Voice Channel',inline=False)
		embed.add_field(name=prf+'meme help',value='See Memes commanands',inline=False)
		embed.add_field(name=prf+'meme random',value='Play Random memes',inline=False)
		embed.add_field(name=prf+'remind help',value='See Reminder commands (Beta)',inline=False)
		embed.add_field(name=prf+'quote help',value='See quote commands',inline=False)
		#embed.add_field(name='.send help',value='See Send commands',inline=False)
		await c.send(embed=embed)
		
	except:
		pass


@b.command(aliases=['r','reminder'])
async def remind(c,*,remind):
	#d,t=[],[]
	if(remind=="help"):
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Reminder')
		embed.add_field(name=prf+'remind <data>  OR  '+prf+'r <data>',value='Used to store reminders and it will notify the person tagged 10 minutes before',inline=False)
		embed.add_field(name='Where <data> is:',value='<Mentions>, <Messages>, <Day/Month/Year>, <Time in 24 hours (Malaysian Time)>',inline=False)
		await c.send(embed=embed)
		return

	try:
		r = [x.strip() for x in remind.split(',')]
		if(len(r) == 4):
			#global d,t,dt
			d = list(map(int, r[2].split('/')))
			t=[r[3][0:2],r[3][2:4]]
			t = list(map(int, t))
			dt = datetime.datetime(year=int(d[2]),month=int(d[1]),day=int(d[0]),hour=int(t[0]),minute=int(t[1]))
			dt = pytz.timezone("Asia/Kuala_Lumpur").localize(dt)
			#,tzinfo=pytz.timezone("Asia/Kuala_Lumpur")
			#pytz.timezone("Asia/Kuala_Lumpur")
			if(len(d)==3 and len(t)==2 and dt>datetime.datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))):
				connect(c.guild.id)
				#insert(r[0],r[1],dt.strftime("%Y-%m-%d %H:%M"))
				insert('From '+c.message.author.mention+' To '+r[0]+' ',r[1],dt.strftime("%Y-%m-%d %H:%M"))
			else:
				embed = discord.Embed(
					colour = discord.Colour.orange()
				)
				embed.set_author(name='Wrong Date or Time')
				embed.add_field(name='Please enter Date or Time that is in the future',value='Seriously? Are you time travelling?\n\nDo '+prf+'"remind help." for reminder help',inline=False)
				await c.send(embed=embed)
	except:
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Wrong Format')
		embed.add_field(name='Please enter according to:',value='<Mentions>, <Messages>, <Day/Month/Year>, <Time in 24 hours (Malaysian Time)>\n\nDo '+prf+'"remind help." for reminnder help',inline=False)
		await c.send(embed=embed)


@b.command(aliases=['q','quotes'])
async def quote(c, find=None):
	if not find:
		#random
		#await c.send(Quote.print())
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.add_field(name='Random Quote',value=Quote.print(),inline=False)
		await c.send(embed=embed)
	elif find == 'anime':
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.add_field(name='Anime Quote',value=Quote.print_anime_quote(),inline=False)
		await c.send(embed=embed)
		#await c.send(Quote.print_anime_quote())
	elif find == 'series':
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.add_field(name='Series Quote',value=Quote.print_series_quote(),inline=False)
		await c.send(embed=embed)
		#await c.send(Quote.print_series_quote())
	elif find == 'help':
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Quote Help')
		embed.add_field(name=prf+'quote',value='Random Quotes',inline=False)
		embed.add_field(name=prf+'quote anime',value='Random anime quote',inline=False)
		embed.add_field(name=prf+'quote series',value='Random series quote',inline=False)
		embed.add_field(name=prf+'quote <search>',value='Where <search> is any keyword you want to search',inline=False)
		embed.add_field(name=prf+'Extra Commands',value='You can also use ".q .." or ".quotes .."',inline=False)
		await c.send(embed=embed)
	else:
		#cari
		qs = qu(find,limit=1)
		#await c.send(qs[0]['quote'] + ' ~' + qs[0]['author'])
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.add_field(name=find+' Quote',value=qs[0]['quote'] + ' ~' + qs[0]['author'],inline=False)
		await c.send(embed=embed)


@b.command()
async def who(c,*,ext):
	if c.author.id == os.getenv('HAPPY'):
		await c.send('You are the most handsome person in this server, Shameer')
	else:
		await c.send('I do not want to answer that')


@b.command()
async def send(c,*sd):
	if len(sd) == 2:
		try:
			message = client.messages.create(
								  body='Message is sent from a Discord Server Called *'+c.message.guild.name+'*. From user named *'+c.message.author.name+'*\n\n*Message:*\n'+sd[1],
								  from_='whatsapp:+14155238886',
								  to='whatsapp:'+str(sd[0])
							  )
		except:
			embed = discord.Embed(
				colour = discord.Colour.orange()
			)
			embed.add_field(name='Sending Problem',value='Please make sure the number entered is valid and the syntax is correct. Do .send help for send help',inline=False)
			await c.send(embed=embed)
	else:
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.set_author(name='Send (beta)')
		embed.add_field(name='.send <number with country code> <space> <messages>',value='Send whatsapp messages to the number entered',inline=False)
		embed.add_field(name='Message Format',value='It will include the name of the server and the discord name of the sender',inline=False)
		await c.send(embed=embed)


b.run(os.getenv('TOKEN'))


#non admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=36781312&scope=bot

#admin
#https://discord.com/api/oauth2/authorize?client_id=783242690435219497&permissions=8&scope=bot
