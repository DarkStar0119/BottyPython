import os
import discord
from discord import Intents
from discord.ext import commands
from keep_alive import keep_alive
import data_access as data
import random as r
import tokens

intents = Intents.all()

#keep_alive()

activity = discord.Activity(type=discord.ActivityType.playing, name="I Seek The Grail")
client = commands.Bot(command_prefix='[]', intents=intents, activity=activity)

stuff = data.loadData()
rolesChannel = 0
groups = stuff[1]
roles = stuff[2]


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  global rolesChannel
  rolesChannel = client.get_channel(stuff[0])

@client.event
async def on_message(message):
  if message.author != client.user:
    ping = r.randrange(100)
    if ping == 69:
      await message.reply("No one expects The Spanish Inquisition!!!")
    elif 'spam' in message.content.lower():
      await message.reply("https://tenor.com/view/monty-python-flying-circus-spam-gif-15349845")
    elif ping == 16:
      await message.channel.send(f'{message.author.mention} has been attacked by a 16 ton weight!!! https://i.gifer.com/Jcrv.gif')
  await client.process_commands(message)

@client.command(name="role",aliases=['r'])
@commands.has_role("Minister")
async def addRoles(ctx, role: discord.Role, emote: str, group: str):
  global rolesChannel
  if str(group) not in groups:
    embed = discord.Embed(title=group)
    newMsg = await rolesChannel.send(embed=embed)
    groups[group] = str(newMsg.id)

  msg = groups[group]
  if msg not in roles:
    roles[msg]={}
  roles[msg][emote] = role.name

  body = ''
  for x in list(roles[msg]):
    body += f'{x} {roles[msg][x]}\r\n'
  embed = discord.Embed(title=group,description=body)
  editable = await rolesChannel.fetch_message(msg)
  await editable.edit(embed=embed)
  data.saveData(rolesChannel.id, groups, roles)
  await editable.add_reaction(emote)
  ctx.message.delete()

@client.event
async def on_raw_reaction_add(payload):
  if payload.user_id != client.user: 
    if str(payload.message_id) in list(groups.values()):
      server = client.get_guild(payload.guild_id)
      user = server.get_member(payload.user_id)
      role = discord.utils.get(server.roles, name=roles[str(payload.message_id)][str(payload.emoji)])
      await user.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
  if payload.user_id != client.user: 
    if str(payload.message_id) in list(groups.values()):
      server = client.get_guild(payload.guild_id)
      user = server.get_member(payload.user_id)
      role = discord.utils.get(server.roles, name=roles[str(payload.message_id)][str(payload.emoji)])
      await user.remove_roles(role)
client.run(tokens.token)