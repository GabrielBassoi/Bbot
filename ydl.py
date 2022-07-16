import os

import discord
import asyncio
import validators

import yt_dlp as yt

from yt_search import SearchYt

ffmpegPath = os.getcwdb().replace(b"\\", b"/").decode("utf-8") + "/ffmpeg-4.4-essentials_build/bin/ffmpeg.exe"

netrcPath = os.getcwdb().replace(b"\\", b"/").decode("utf-8") + "/test.netrc"

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s-%(duration)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'netrc': True,
    'netrc-location': netrcPath
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt.YoutubeDL(YDL_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def get_info(cls, text, loop=None, stream=False):
        url = ""

        if validators.url(text):
            url = text
        else:
            url = SearchYt.search(text)

        try:
            loop = loop or asyncio.get_event_loop()
            data = ytdl.extract_info(url, download=not stream)

            if 'entries' in data:
                data = data['entries'][0]

            return data
        except:
            print("Ocorreu um erro")

    @classmethod
    def init_player(cls, data, stream=False):
        try:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except:
            print("Ocorreu um erro")

'''executable=ffmpegPath,''' # With in pc put on return cls(... , with send to heroku remove
