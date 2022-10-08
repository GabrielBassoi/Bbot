import discord
from discord.ext import commands
import music as music
import ffmpeg
from boto.s3.connection import S3Connection
import os

cogs = [music]

client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

token = ''

for i in range(len(cogs)):
    cogs[i].setup(client)

# token = S3Connection()
# token = S3Connection(os.environ['TOKEN'])

client.run("ODg3MDgzNTE1NzEwMTYwOTE3.GFwrKk.rShcrrIQUW1ZBuxVS_XhYL90ThlvAIib81s0FY")
