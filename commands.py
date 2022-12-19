import asyncio
import datetime
from ydl import YTDLSource
from discord.ext import commands

help_text = '''
Bot commands:

🎶 - p [url/name]            | Play the music/video
😁 - join                              | Join in the current channel
😥 - disconnect                | Disconnect from the current channel
🔊 - volume [0-1000]    | Change the output volume
⏯ - pr                                | Toggle between paused and playing
⏹ - stop                            | Stop the current track and disconnect
📃 - list                              | Show the playlist
⏩ - skip                            | Play the next music/video
♾ - loop                            | L∞P
😎 - festourado                | FOOOOOOOOOOOOOOOORGET
'''
playlist_empty_text = "The playlist is empty"
no_music_playing_text = "There's no music playing ;("

is_loop = False
paused = False
musics: list = []


class Commands:

    async def join(self, self_music, ctx):
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    async def disconnect(self, self_music, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    async def play_music(self, self_music, ctx, text):
        data = await YTDLSource.get_info(text)
        musics.append(data)

        if not ctx.voice_client.is_playing() and len(musics) > 1:
            await ctx.send(f'{data.get("title")} | Added to the list!')
            await play(self_music, ctx, musics[0])
        elif not ctx.voice_client.is_playing() and len(musics) == 1:
            await play(self_music, ctx, musics[0])
        else:
            await ctx.send(f'{data.get("title")} | Added to the list!')

    async def pause_resume(self, self_music, ctx):
        global paused
        if await verify_is_music_empty(ctx):
            if ctx.voice_client.is_playing():
                await pause(ctx)
            elif not ctx.voice_client.is_playing():
                await resume(ctx)
            else:
                await ctx.send(no_music_playing_text)

    async def change_volume(self, self_music, ctx, volume):
        if ctx.voice_client.is_playing() and await verify_is_music_empty(ctx):
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f'Changed volume to {volume}%')
        else:
            await ctx.send(no_music_playing_text)

    async def stop(self, self_music, ctx):
        musics.clear()
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    async def help(self, self_music, ctx):
        await ctx.send(help_text)

    async def show_list(self, self_music, ctx):
        if await verify_is_music_empty(ctx):
            text = "Playlist:\n"
            for n in range(len(musics)):
                text += f'{n} | {musics[n].get("title")} | {format_duration(musics[n].get("duration"))}\n'
            await ctx.send(text)

    async def skip_music(self, self_music, ctx):
        global is_loop, paused

        if await verify_is_music_empty(ctx):
            if is_loop:
                is_loop = False
                await ctx.send("Loop is false")
            paused = False
            ctx.voice_client.stop()

    async def festourado(self, self_music, ctx):
        if ctx.voice_client.is_playing() and await verify_is_music_empty(ctx):
            ctx.voice_client.source.volume = 10000 / 100
            await ctx.send(f'Forget estourado 🤏😎🤏😎')
        else:
            await ctx.send(no_music_playing_text)

    async def loop(self, self_music, ctx):
        global is_loop
        if is_loop:
            is_loop = False
        else:
            is_loop = True

        await ctx.send(f"Loop is {str(is_loop).lower()}")

    async def exit(self, self_music, ctx):
        if ctx.author.id == 320505702919700483:
            await ctx.send("Bye bye")
            await ctx.voice_client.disconnect()
            exit(0)
        else:
            await ctx.send("kk tu nao eh o ademir 🥵🥵🥵")


async def play(self, ctx: commands.Context, data, stream=False):
    global paused, is_loop

    async def init_player():
        while True:
            player = YTDLSource.init_player(data)
            if not is_loop:
                await ctx.send(f'Now playing: {player.title}')
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            try:
                while ctx.voice_client.is_playing() or paused:
                    await asyncio.sleep(1)
            except AttributeError:
                print("Bot stopped")
            if not is_loop:
                break

    await init_player()
    await iter_musics(self, ctx)


async def iter_musics(self, ctx):
    if verify_voice_client(ctx):
        musics.pop(0)
        if ctx.voice_client is not None and len(musics) != 0:
            await play(self, ctx, musics[0])
        elif ctx.voice_client is not None:
            await ctx.send(playlist_empty_text)


def verify_voice_client(ctx):
    if ctx.voice_client is None:
        return False
    else:
        return True

def format_duration(seconds):
    time = str(datetime.timedelta(seconds=seconds))
    timestamp = time.split(":")
    if timestamp[0] != "0":
        return f"{timestamp[0]}:{timestamp[1]}:{timestamp[2]}"
    return f"{timestamp[1]}:{timestamp[2]}"


async def verify_is_music_empty(ctx):
    if len(musics) != 0:
        return True
    await ctx.send(playlist_empty_text)
    return False


async def pause(ctx):
    global paused

    paused = True
    ctx.voice_client.pause()
    await ctx.send("Paused ⏸")


async def resume(ctx):
    global paused

    paused = False
    ctx.voice_client.resume()
    await ctx.send("Resume ▶")