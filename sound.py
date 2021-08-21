    from __future__ import unicode_literals
import discord
import urllib.request
import re
import youtube_dl
import asyncio
from discord.ext import commands


class Sound(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ext 1 succefully loaded')

    @commands.command()
    async def play(self, ctx, *, search):
        if ctx.author.voice is None:
            await ctx.send('you are not in voice channel')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
   
        else:
            ctx.voice_client.move_to(voice_channel)
        #For matching diffrences of url and string title
        match = re.findall(r'watch\?v=(\S{11})', search)
        if match:
            url = search
        # If match doesnt find it will converted to string title
        else:
            data = re.sub('\s', '+', search)
            html = urllib.request.urlopen(f'http://www.youtube.com/results?search_query={data}')
            video_ids = re.findall(r'watch\?v=(\S{11})',html.read().decode())
            extract = (video_ids[1])
            url = ('http://www.youtube.com/watch?v='+ extract)

        ctx.voice_client.stop()
        FFMPEG_OPTS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download= False)
            video_title = info.get('title', None) 
            url2 = info['formats'][0]['url']
            src = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTS)
            await ctx.send(f'**Now Playing :**{video_title}')
            vc.play(src)
            print(data)
            print(extract)

    @commands.command(help = 'To stop bot and leave voice channel ')
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        
    @commands.command(help = 'To pause your music')
    async def pause(self, ctx):
      await ctx.send('**music paused**')
      await ctx.voice_client.pause() 
    
    @commands.command(help = 'Resume again')
    async def resume(self, ctx):
      await ctx.send('**music resumed**')
      await ctx.voice_client.resume()
      
#def setup(client):
    client.add_cog(Sound(client))
