import discord
from discord.ext import commands
import music as music
import asyncio

cogs = [music]

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())


async def main():
    for i in range(len(cogs)):
        await cogs[i].setup(client)


asyncio.run(main())

client.run("ODg3MDgzNTE1NzEwMTYwOTE3.GFwrKk.rShcrrIQUW1ZBuxVS_XhYL90ThlvAIib81s0FY")
