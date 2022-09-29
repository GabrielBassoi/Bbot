import discord
from discord.ext import commands
import music as music
import ffmpeg
from boto.s3.connection import S3Connection

cogs = [music]

client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

token = ''

for i in range(len(cogs)):
    cogs[i].setup(client)

token = S3Connection(os.environ['TOKEN'])

client.run(token)
