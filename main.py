import discord
from discord.ext import commands
import music as music
import ffmpeg

cogs = [music]

client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run('ODg3MDgzNTE1NzEwMTYwOTE3.YT--5w.FSDobIS2mpXem8C2-Os07a6_tIc')
