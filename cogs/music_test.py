
from discord.ext import commands, tasks
import lavalink
import asyncio
import re
import typing
from utils.interface import *
import discord

from .music_base import Music_base
url_rx = re.compile(r'https?://(?:www\.)?.+')
time_rx =re.compile('[0-9]+')

class Music_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_base = self.bot.get_cog('Music_base')

    @commands.command(aliases=['insert', 'i'])
    async def insert_track(self, ctx, track_index :typing.Optional[int]=0, *, query:str):

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not url_rx.match(query.strip('<>')):
            query = f'ytsearch:{query +" lyrics"}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

         # playlist   
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                await self.music_base.insert_player_song(ctx, track, track_index)
            embed = discord.Embed(
            title=f"{results['playlistInfo']['name']}" ,
            colour=color.green
            )


        else:
            track = results['tracks'][0]
            await self.music_base.insert_player_song(ctx , track, track_index)
            embed = discord.Embed(
            title=f"{track['info']['title']}" 
            ,url=f"{track['info']['uri']}",
            colour=color.orange
            )
        embed.set_author(name=f"inserted tracks")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['forceskip', 'fs'])
    async def skip(self, ctx, amount: int=None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if amount is None:
            amount = 1
        else:
            amount = amount
        if not player.is_playing:
            return await ctx.send('I`m not playing.')
        if amount > len(player.queue):
            await ctx.send(':warning: Invalid number of skip')
        else:
            await ctx.send('music skipped')
            for i in range(amount):
                await player.skip()
            await self.music_base.playernow_song(ctx)
            
    @commands.command(aliases=['clear'])
    async def clear_queue(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
       
        if not player.is_connected:
            embed = discord.Embed(title=":warning: I'm not connected to any voice channels", colour=color.red)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed = discord.Embed(title=":warning: Please join in my channel first", colour=color.red)
        embed = discord.Embed(title=f"{len(self.guild_queues[ctx.guild.id])} track has been cleared",colour=color.red)
        player.queue.clear()
        
        await self.music_base.clear_list(ctx)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Music_utils(bot))