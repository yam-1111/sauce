import discord
import asyncio
from discord.ext import commands

class Sound(commands.Cog):
	def __init__(self, client):
		self.client = client
		
	@commands.Cog.listener()
	async def on_ready(self):
		print('ext 1 succefully loaded')
	@commands.command()
	async def play(self, ctx, url):
		if ctx.author.voice is None:
			await ctx.send('Wala ka sa channel tanga')
		voice_channel = ctx.author.voice.channel
		if ctx.voice_client is None:
			await voice_channel.connect()
		else:
			ctx.voice_client.move_to(voice_channel)
		
		ctx.voice_client.stop()
		FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		YDL_OPTS = {'format': 'bestaudio'}
		vc = ctx.voice_client
		with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
			info = ydl.extract_info(url, download= false)
			url2 = info['formats'][0]['url']
			src = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTS)
			vc.play(src)
	@commands.command()
	async def stop(self, ctx):
		await ctx.voice_client.disconnect()
		
	
		
		
			
def setup(client):
	client.add_cog(Sound(client))