from discord.ext import commands
import commands as cmd

not_in_channel_text = "I'm not in a voice channel"
user_not_in_channel_text = "You're not in a voice channel"


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.commands = cmd.Commands()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send(user_not_in_channel_text)
        else:
            await self.commands.join(self, ctx)

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.disconnect(self, ctx)

    @commands.command()
    async def p(self, ctx: commands.Context, *, text):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        await self.commands.play_music(self, ctx, text)

    @commands.command()
    async def unf(self, ctx):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        await self.commands.play_music(self, ctx, "https://www.youtube.com/watch?v=oWTZTCl_QW8")

    @commands.command()
    async def pr(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send(not_in_channel_text)
        else:
            await self.commands.pause_resume(self, ctx)

    @commands.command()
    async def volume(self, ctx, volume: int = 50):
        if ctx.voice_client is None:
            return await ctx.send(not_in_channel_text)
        else:
            await self.commands.change_volume(self, ctx, volume)

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.stop(self, ctx)

    @commands.command()
    async def h(self, ctx):
        await self.commands.help(self, ctx)

    @commands.command()
    async def list(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.show_list(self, ctx)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.skip_music(self, ctx)

    @commands.command()
    async def festourado(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send(not_in_channel_text)
        else:
            await self.commands.festourado(self, ctx)

    @commands.command()
    async def loop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.loop(self, ctx)

    @commands.command()
    async def exit(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(not_in_channel_text)
        else:
            await self.commands.exit(self, ctx)


async def setup(client):
    await client.add_cog(Music(client))
