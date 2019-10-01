__version__ = "1.0.2"

import discord
from discord import utils, Client
from discord.ext import commands
from discord.utils import find
from cogs.utils import checks, perms
import logging
import random
import os
import typing
import json
import datetime
import aiohttp
import sqlite3
import sys
import traceback
import asyncio
import calendar
import time
from random import randrange

client = commands.Bot(
           command_prefix="/",
           description="Bossy Bot",
           owner_id=467306557114155018,
           case_insensitive=True
)
client.remove_command('help')

	
@client.command(name="load", discription="Loads a cog", hidden=True)
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")
	await ctx.send('Successfully loaded')
	
@client.command(hidden=True)
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	await ctx.send('Successfully unloaded')
	
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
	print("Pretty Neat bot is launching")
	game = discord.Game("Launchin zzz..")
	await client.change_presence(status=discord.Status.idle, activity=game)
	print("Launched sucessfully" + client.user.display_name)
	game1 = discord.Game("/help | by Héx#6542")
	await client.change_presence(status=discord.Status.online, activity=game1)
		
	
@client.event
async def on_guild_join(guild):
	general = find(lambda x: x.name == 'general', guild.text_channels)
	if general and general.permissions_for(guild.me).send_messages:
		embed = discord.Embed(title=f"Thanks for Adding me on {guild}", description="To know list of commands, Please type /help , Made by ``héx#6542`` ", color=discord.Color.greyple(), timestap=datetime.datetime.utcnow())
		embed.add_field(name="Total servers", value=len(client.guilds))
		await general.send(embed=embed)
	
@client.command()
async def welcomer_help(ctx):
	embed = discord.Embed(color=discord.Color.dark_teal())
	embed.add_field(name="Available Setup Commands", value="`welcomer set_channel` | `welcomer set_text`")
	embed.add_field(name="Available Format for Text", value="`mention` - Mentions the member | `user` - Shows the member name | `guild` - Shows the guild name")
	await ctx.send(embed=embed)
	
@client.command()
async def help(ctx):
	embed = discord.Embed(color=discord.Color.dark_teal(), timestap=datetime.datetime.utcnow())
	embed.add_field(name="General Commands", value="*ping | av | userav | userinfo | guildinfo | welcomer | embed | bitcoin | serverstats | joined | uptime | botinfo*", inline=True)
	embed.add_field(name="Mathematics Commands", value="*add | subtract | multiply | divide*", inline=True)
	embed.add_field(name="Fun Commands", value="*meme | slap | mentionme | dice | rps | toss | reverse | cat | dog | hug*", inline=True)
	embed.add_field(name="Search Commands", value="*google | youtube | yahoo*", inline=True)
	embed.add_field(name="Action Commands", value="*ban | unban |add_role | kick | purge | mute | unmute | softban*", inline=True)
	await ctx.send(embed=embed)
	
	
	
@client.command()
@commands.is_owner()
async def logout(ctx):
	print('Logged Out')
	async with ctx.typing():
		await ctx.send("Logged out successfully")
		await client.logout()
		print('Done')
		
@client.command()
@commands.is_owner()
async def connect(ctx):
	print("Connecting...")
	await client.connect(reconnect=True)
	print("Connected" + (len(client.guilds)))
	
@client.command()
@commands.is_owner()
async def stats(ctx):
	await ctx.send(len(client.commands) + len(client.guilds) + len(client.users))
	
@client.command()
async def ping(ctx):
	msg = f"My latency is {round(client.latency * 1000)}ms"
	embed = discord.Embed(title="Pong :ping_pong:", description=msg, color=discord.Color.green())
	await ctx.send(embed=embed)
	
@client.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
    
@client.command()
async def av(ctx):
	show_avatar = discord.Embed(
	
	         color = discord.Color.blue()
	)
	show_avatar.set_image(url="{}".format(ctx.author.avatar_url))
	await ctx.send(embed=show_avatar)

@client.command()
async def userav(ctx, member : discord.Member):
	show_avatar = discord.Embed(
	
	         color = discord.Color.dark_blue()
	)
	show_avatar.set_image(url="{}".format(member.avatar_url))
	await ctx.send(embed=show_avatar)
	
@client.command()
async def userinfo(ctx, member: discord.Member):
	roles = [role for role in member.roles]
	
	em = discord.Embed(title=f"Userinfo - {member.name}", description=f"Shows Info about {member.name}", color=discord.Color.dark_orange(), timestap=datetime.datetime.utcfromtimestamp(1553629094))
	em.set_thumbnail(url=f"{member.avatar_url}")
	em.add_field(name="ID:", value=member.id)
	em.add_field(name="Guild_Name:", value=member.display_name)
	
	em.add_field(name="Created_at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name="Joined_at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
	em.add_field(name="Top Role", value=member.top_role.mention)
	em.add_field(name="Bot?", value=member.bot)
	
	await ctx.send(embed=em)
	
@client.command()
async def guildinfo(ctx):
	roles = [role for role in ctx.guild.roles]
	guild_age = (ctx.message.created_at - ctx.author.guild.created_at).days
	created_at = f"Server created on {ctx.author.guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
	online = len({m.id for m in ctx.author.guild.members if m.status is not discord.Status.offline})
	em = discord.Embed(title=f"Guild Info - {ctx.guild.name}", description=created_at, color=discord.Color.blurple())
	em.set_thumbnail(url=ctx.author.guild.icon_url)
	em.set_author(name="Guild Info", icon_url=ctx.author.guild.icon_url)
	em.add_field(name="Name:", value=ctx.author.guild.name)
	em.add_field(name="Id:", value=ctx.author.guild.id)
	em.add_field(name="Online:", value=online)
	em.add_field(name="Total Members:", value=len(ctx.author.guild.members))
	em.add_field(name="Owner:", value=ctx.guild.owner)
	em.add_field(name="Roles:", value=len(roles))
	em.add_field(name="Emojis:", value=len(ctx.guild.emojis))
	em.add_field(name="Region", value=ctx.guild.region)
	em.add_field(name="Verification level", value=ctx.guild.verification_level)
	em.add_field(name="Text Channels:", value=len(ctx.guild.text_channels))
	em.add_field(name="Voice Channs:", value=len(ctx.guild.voice_channels))
	await ctx.send(embed=em)
	
@client.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])
        
@client.command()
async def cat(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get('http://aws.random.cat/meow') as r:
			if r.status == 200:
				js = await r.json()
				await ctx.send(js['file'])

				
@client.command(pass_context=True)
async def dog(ctx):
    username = ctx.message.author.display_name
    passlist = [
    'https://images.pexels.com/photos/356378/pexels-photo-356378.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
    'https://3c1703fe8d.site.internapcdn.net/newman/gfx/news/hires/2018/2-dog.jpg',
    'https://www.petmd.com/sites/default/files/Acute-Dog-Diarrhea-47066074.jpg',
    'https://www.gannett-cdn.com/-mm-/eaf5fe27686b5cce643ad02955079d0247a7259e/c=304-0-4660-3275/local/-/media/2018/07/11/NJGroup/AsburyPark/636669276528789207-remy071118a.jpg',
    'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/german-shepherd-dog-smiling-outdoors-royalty-free-image-529202089-1557354659.jpg?crop=0.668xw:1.00xh;0.167xw,0&resize=640:*',
    'https://www.what-dog.net/Images/faces2/scroll0015.jpg',
    'https://static-cdn.jtvnw.net/jtv_user_pictures/dogdog-profile_image-5550ade194780dfc-300x300.jpeg',
    'https://www.adorama.com/alc/wp-content/uploads/2018/02/shutterstock_526957903.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDmRUrH1pwyW4pCUfc5De9mzlLGwk7WXTByfHN0jrxGd0q4hXJ',
    'https://www.what-dog.net/Images/faces2/scroll008.jpg',
    'http://www.doglivingmagazine.com/wp-content/uploads/2018/04/shadyside-inn-dogs-front-desk-300x160.jpg',
    'http://www.directexpose.com/wp-content/uploads/2018/02/cf53f9b5-24.-pomeranian-rare-dog-breeds-buzzfeed.jpg',
        ]
    embed=discord.Embed(title="A Cute Image of A Dog", color=0x00ff80)
    embed.set_author(name="Patwarded®", icon_url="https://vetstreet-brightspot.s3.amazonaws.com/3a/54/5ae8bfcc41b381c27a792e0dd891/AP-KWDHXS-645sm8113.jpg")
    embed.set_footer(text="Requested by " + username )
    chooser1 = random.choice((passlist))
    embed.set_image(url=chooser1)
    await ctx.send(embed = embed)
	
	
@client.command()
async def botinfo(ctx):
	platform = sys.platform
	guilds = len(client.guilds)
	embed = discord.Embed(color=discord.Color.dark_green(), description="Hii! Im **BossyBot** the official bot of Bossy server. Héx#6542 is my Daddy.")
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.add_field(name="Library", value="discord.py")
	embed.add_field(name="Commands Injected", value=len(client.commands))
	embed.add_field(name="Platform", value=platform)
	embed.add_field(name="Guilds", value=guilds)
	embed.add_field(name="Used by", value=len(client.users))
	await ctx.send(embed=embed)


@client.command()
async def mentionme(ctx):
	await ctx.send(ctx.author.mention + "Mentioned You")
	
@client.command()
async def serverstats(ctx):
	bots = 0
	members = 0
	total = 0
	for x in ctx.guild.members:
		if x.bot == True:
			bots += 1
			total += 1
		else:
			members += 1
			total += 1
	embed = discord.Embed(title="Server Stats", color=discord.Color.dark_red())
	embed.add_field(name="Bot Count", value=f'{bots}', inline=True)
	embed.add_field(name="Member Count", value=f'{members}', inline=True)
	embed.add_field(name="Total Count", value=f'{total}', inline=True)
	await ctx.send(embed=embed)
	
@client.command()
async def dice(ctx):
	await ctx.send(f"{ctx.author.display_name}, you rolled **{randrange(1, 7)}**!")
	
@client.command()
async def toss(ctx):
	choice = random.randint(1,2)
	if choice == 1:
		await ctx.send("Heads")
	else:
		await ctx.send("Tails")
		
@client.command()
async def meme(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.reddit.com/r/me_irl/random") as r:
			data = await r.json()
			await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
			
@client.command()
async def reverse(ctx, *, message):
	message = message.split()
	await ctx.send(' '.join(reversed(message)))
	
@client.command()
async def slap(ctx, *, member: discord.Member = None):
	if member is None:
		embed = discord.Embed(color=discord.Color.dark_teal(), title="No One to slap 🙄", description="You have to mention any member to slap that fellow human.")
		embed.set_thumbnail(url="https://i.imgur.com/6YToyEF.png")
		await ctx.send(embed=embed)
	elif member.id == ctx.message.author.id:
		embed = discord.Embed(title="What You want to slap you 🤔", description="No I can't slap you because you are my friend", color=discord.Color.dark_green())
		embed.set_image(url="http://4.bp.blogspot.com/-FL6mKTZOk94/UBb_9EuAYNI/AAAAAAAAOco/JWsTlyInMeQ/s400/Jean+Reno.gif")
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Slapped", description=f"**{ctx.author} slapped {member}**", color=discord.Color.dark_red())
		embed.set_image(url="https://media0.giphy.com/media/l2YOqzhYD066fAd56/giphy.gif")
		await ctx.send(embed=embed)
		
@client.command()
async def hug(ctx, *, member: discord.Member = None):
	if member is None:
		await ctx.send(f"{ctx.message.author.mention} has been hugged 💝")
	elif member.id == ctx.message.author.id:
		await ctx.send(f"{ctx.message.author.mention} hugged themselves because they are singles 👬")
	else:
		await ctx.send(f"{member.mention} was hugged by  {ctx.message.author.mention} 💝")
		
@client.command()
async def google(ctx, *, search = None):
	if search == None:
		embed = discord.Embed(titile="Google Serch error", description="Nothing to search", color=discord.Color.blue())
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=f"{search}", color=discord.Color.dark_blue(), url=f"https://www.google.com/search?q={search}")
		embed.set_author(name="Google Search", icon_url="https://cdn.discordapp.com/attachments/600914805619949588/601930101952741377/google-logo-icon-PNG-Transparent-Background-768x768.png")
		await ctx.send(embed=embed)
		
@client.command()
async def yahoo(ctx, *, search = None):
	if search == None:
		embed = discord.Embed(title="Yahoo Search Error", description="Cannot Find anything", color=discord.Color.dark_red())
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=f"**{search}**", color=discord.Color.blurple(), url=f"https://in.search.yahoo.com/search?p={search}")
		embed.set_author(name="Yahoo Search", icon_url="https://cdn.discordapp.com/attachments/625273073330946058/625281245709991936/58482919cef1014c0b5e49f3.png")
		await ctx.send(embed=embed)
		
@client.command()
async def youtube(ctx, *, search = None):
	if search == None:
		embed = discord.Embed(title="YouTube Search error", description="Nothing to search", color=discord.Color.dark_red())
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title=f"**{search}**", color=discord.Color.blurple(), url=f"https://www.youtube.com/results?search_query={search}")
		await ctx.send(embed=embed)
@client.command()
async def add_role(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.permissions_in(ctx.channel).kick_members or ctx.author.permissions_in(ctx.channel).manage_messages:
        await member.add_roles(role)
    else:
        e = discord.Embed(title='Denied', colour=discord.Colour.gold(), description=f'''{ctx.author.mention} you aren't eligible for this''')
        await ctx.send(embed=e)
        
@client.command(pass_context=True)
async def rps(ctx, choice):
    choices = ["rock", "paper", "scissors"]
    await ctx.send("You chose {} | CPU chose {}".format(choice, random.choice(choices)))
    
client.run(os.getenv('TOKEN'))	
    


        

