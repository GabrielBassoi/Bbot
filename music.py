import asyncio
import datetime

from ydl import YTDLSource

import discord
from discord.ext.commands import bot
from discord.ext import commands

musics: list = []

help_text = '''
Bot commands:

🎶 - p [url/name]            | Play the music/video
😁 - join                              | Join in the current channel
🤓 - disconnect                | Disconnect from the current channel
🔊 - volume [0-1000]    | Change the output volume
⏯ - pr                                | Toggle between paused and playing
⏹ - stop                            | Stop the current track and disconnect
📃 - list                              | Show the playlist
⏩ - skip                            | Play the next music/video
♾ - loop                            | L∞P
😎 - festourado                | FOOOOOOOOOOOOOOOORGET
'''

is_loop = False
paused = False


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice = after.channel.guild.voice_client
        time = 0
        while True:
            await asyncio.sleep(1)
            time = time + 1
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 300:
                await voice.disconnect()
            if not voice.is_connected():
                break

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
            if musics != 0:
                await play(self, ctx, musics[0])
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
        else:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()

    @commands.command()
    async def p(self, ctx: commands.Context, *, text):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        data = await YTDLSource.get_info(text)
        musics.append(data)

        if not ctx.voice_client.is_playing() and len(musics) > 1:
            await ctx.send(f'{data.get("title")} | Added to the list!')
            await play(self, ctx, musics[0])
        elif not ctx.voice_client.is_playing and len(musics) == 1:
            await play(self, ctx, musics[0])
        else:
            await ctx.send(f'{data.get("title")} | Added to the list!')


    @commands.command()
    async def pr(self, ctx):
        global paused
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel!")
        else:
            if ctx.voice_client.is_playing() and len(musics) != 0:
                paused = True
                ctx.voice_client.pause()
                await ctx.send("Paused ⏸")
            elif not ctx.voice_client.is_playing() and len(musics) != 0:
                paused = False
                ctx.voice_client.resume()
                await ctx.send("Resume ▶")
            else:
                await ctx.send("There's no music playing ;(")

    @commands.command()
    async def volume(self, ctx, volume: int = 50):
        if ctx.voice_client is None:
            return await ctx.send("I'm not in a voice channel!")
        else:
            if ctx.voice_client.is_playing() and len(musics) != 0:
                ctx.voice_client.source.volume = volume / 100
                await ctx.send(f'Changed volume to {volume}%')
            else:
                await ctx.send("There's no music playing ;(")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel")
        else:
            musics.clear()
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()

    @commands.command()
    async def h(self, ctx):
        await ctx.send(help_text)

    @commands.command()
    async def list(self, ctx):
        if ctx.voice_client is None:
            ctx.send("I'm not in a voice channel")
        else:
            if len(musics) != 0:
                text = "Playlist:\n"
                for n in range(len(musics)):
                    text += f'{n} | {musics[n].get("title")} | {format_duration(musics[n].get("duration"))}\n'
                await ctx.send(text)
            else:
                await ctx.send("The playlist is empty")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            ctx.send("I'm not in a voice channel")
        else:
            if len(musics) > 1:
                ctx.voice_client.stop()
            else:
                await ctx.send("The playlist is empty")

    @commands.command()
    async def festourado(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Not connected to a voice channel.")
        else:
            if ctx.voice_client.is_playing() and len(musics) != 0:
                ctx.voice_client.source.volume = 10000 / 100
                await ctx.send(f'Forget estourado 🤏😎🤏😎')
            else:
                await ctx.send("There's no music playing ;(")

    @commands.command()
    async def loop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Not connected to a voice channel.")
        else:
            await set_loop(ctx)

    @commands.command()
    async def exit(self, ctx):
        user = ctx.author.id
        if user == 320505702919700483:
            exit(0)
        else:
            await ctx.send("kk tu nao eh o adm 🤏🤏🥺")


def setup(client):
    client.add_cog(music(client))


async def play(self, ctx: commands.Context, data, stream=False):
    global paused
    global is_loop

    async def loop_play():
        while is_loop:
            player = YTDLSource.init_player(data)
            ctx.voice_client.play(player)

            while ctx.voice_client.is_playing() or paused:
                await asyncio.sleep(1)

    async def player():
        player = YTDLSource.init_player(data)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: {player.title}')

        while ctx.voice_client.is_playing() or paused:
            await asyncio.sleep(1)

    if is_loop:
        await loop_play()
    else:
        await player()

    await iter_musics(self, ctx)


async def iter_musics(self, ctx):
    musics.pop(0)

    if len(musics) != 0:
        await play(self, ctx, musics[0])
    else:
        await ctx.send("The playlist is empty")


async def set_loop(ctx):
    global is_loop
    if is_loop:
        is_loop = False
    else:
        is_loop = True

    await ctx.send(f"Loop is {is_loop}")


def format_duration(seconds):
    time = str(datetime.timedelta(seconds=seconds))
    l = time.split(":")
    if l[0] != "0":
        return f"{l[0]}:{l[1]}:{l[2]}"
    return f"{l[1]}:{l[2]}"