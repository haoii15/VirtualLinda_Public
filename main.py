import discord
import kjellar.kjellar_msg as kjellar
import haoii.main as haoii
import idfetch

from config import GUILDID, HAOIIID
from kjellar.config import ROLEMSGID

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.emoji_to_role = {
		848251641433423942 : 848252507502280734,
		808698167029006376 : 848252323989422110,
		840310204460564500 : 893202149998227506,
		893206008153911328 : 803254738300436552,
		979670101689270322 : 954290914665328680
		}

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents = intents)
users = []

clientid = idfetch.fetchid()

@client.event

async def on_ready():
  	print("We have logged in as {0.user}".format(client))

@client.event

async def on_message(message):
	if message.author == client.user or message.author.bot == True:
		return

	if message.guild.id == GUILDID:
		await kjellar.newMessage(client, message)
	elif message.guild.id == HAOIIID:
		await haoii.newMessage(client, message)

@client.event
 
async def on_raw_reaction_add(payload):
	if payload.message_id != ROLEMSGID:
		return

	guild = client.get_guild(GUILDID)
	if guild == None:
		return

	try:
		role_id = client.emoji_to_role[payload.emoji.id]
	except KeyError:
		return

	role = guild.get_role(role_id)
	if role == None:
		return
  
	if "Bots" not in payload.member.roles:
		await payload.member.add_roles(role)

@client.event

async def on_raw_reaction_remove(payload):
	if payload.message_id != ROLEMSGID:
		return

	guild = client.get_guild(GUILDID)
	if guild == None:
		return

	try:
		role_id = client.emoji_to_role[payload.emoji.id]
	except KeyError:
		return

	role = guild.get_role(role_id)
	if role == None:
		return

	member = guild.get_member(payload.user_id)
	if member == None:
		return
	else:
		await member.remove_roles(role)

@client.event

async def on_member_join(member):
	if member.guild.id == GUILDID:
		await kjellar.joined(member)

client.run(clientid)