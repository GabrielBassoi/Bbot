import discord
from discord.ext import commands
import music as music
import ffmpeg

cogs = [music]

client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

token = ''

for i in range(len(cogs)):
    cogs[i].setup(client)

with open('token.txt', 'r') as f:
    token = f.read()

client.run(token)
