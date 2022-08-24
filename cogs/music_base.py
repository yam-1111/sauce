
import asyncio
import re
import math
import discord
import lavalink
import typing
from discord.ext import commands, tasks
from settings.base_config import discord_config
from utils.interface import *
from utils.util_lavaplayer import LavalinkVoiceClient

from settings.config import server
server = server

url_rx = re.compile(r'https?://(?:www\.)?.+')
time_rx =re.compile('[0-9]+')

class Music_base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_queues = {}
        self.guild_autoplay = {}
        self.guild_db()
        if not hasattr(
            bot, "lavalink"
        ):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node(
                server.host,
                server.port,
                server.password,
                server.country,
                server.type_node,
                None, 
                server.resume_timeout,
                server.reconnect_times,
                server.ssl
                
            )  # Host, Port, Password, Region, Name
            lavalink.add_event_hook(self.track_hook)
    def guild_db(self):
            for guild in self.bot.guilds:
                self.guild_queues[guild.id] = []
                self.guild_autoplay[guild.id] = False
    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')
        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')
            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    # cmds
    async def insert_player_song(self, ctx, track, track_index):
        guildqueue = self.guild_queues[ctx.guild.id]
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        self.guild_queues[ctx.guild.id].insert(guildqueue.index(player.current.uri)+(track_index+1), track['info']['uri'])
        player.add(requester=ctx.author.id, track=track, index=track_index)

    async def player_song(self, ctx, track):
        self.guild_queues[ctx.guild.id].append(track['info']['uri'])
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.add(requester=ctx.author.id, track=track)

    @commands.command(aliases=['now'])
    async def playernow_song(self, ctx):
        print(self.guild_queues, self.guild_autoplay)
        song = await self.get_queue(ctx)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        print('statement exce')      
        
        embed = discord.Embed(colour=color.fuchsia, 
        title=player.current.title[:45] + "..."if len(player.current.title)>45 else player.current.title, 
        url=player.current.uri)

        embed.set_author(name=f'{self.guild_queues[ctx.guild.id].index(player.current.uri)+1} / {len(self.guild_queues[ctx.guild.id])} Now Playing',icon_url=ui.yt)
        embed.add_field(
            value=f'Next song : {song} ', inline=True,
            name=f'{mechanism.ms_duration(player.current.duration, player.current.stream)} {await self.player_system_interface(ctx)}'
            )
        #images 
        embed.set_thumbnail(url=photos.icon(player.current.uri))
        embed.set_image(url=photos.thumbnail(player.current.uri))
        await ctx.send(embed=embed)

    async def clear_playlist(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        for song in self.guild_queues[ctx.guild.id]:
            if song != player.current.uri:
                self.guild_queues[ctx.guild.id].remove(song)

    async def player_system_interface(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        def is_loop():
            if player.repeat:
                return '✅'
            return '⛔'
        def is_auto():
            if self.guild_autoplay[ctx.guild.id] is True:
                return '✅'
            return '⛔'
        def is_volume():
            return player.volume

        return f"   🔁loop|{is_loop()}    🤖autoplay|{is_auto()}   🔊volume|{is_volume()}%"
    async def get_queue(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        print(player.queue)
        if len(player.queue) == 0:
            song_name = 'no queue yet..'
            return song_name
        else:
            song = player.queue[0]
            song_name = song.title
            return song_name
    #commands
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query +" lyrics"}'
        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                await self.player_song(ctx, track)
            embed = discord.Embed(
            title=f"{results['playlistInfo']['name']}" ,
            colour=color.green
            )
            embed.set_author(name=f"💿 Playlist - {len(tracks)} ")
        else:
            track = results['tracks'][0]
            await self.player_song(ctx, track)
            embed = discord.Embed(
            title=f"{track['info']['title']}" 
            ,url=f"{track['info']['uri']}",
            colour=color.orange
            )
            embed.set_author(name=f"💿 positioned at {len(player.queue)}")
        embed.set_footer(text=f'requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        if not player.is_playing:
            print('cell active')
            await player.play()
            await self.playernow_song(ctx)



    @commands.command(aliases=['stop', 'dc', 's'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed = discord.Embed(title=":warning: I'm not connected to any voice channels", colour=color.red)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed = discord.Embed(title=":warning: Please join in my channel first", colour=color.red)
        
        # Disconnect from the voice channel.
        self.guild_queues[ctx.guild.id].clear()
        self.guild_autoplay.update({ctx.guild.id : False})
        player.queue.clear()
        await player.stop()
        await ctx.voice_client.disconnect(force=True)
        embed = discord.Embed(title=" :octagonal_sign: Succefully Disconnected", colour=color.green)
        await ctx.send(embed=embed)


     #autoplay command
    async def capture_track(self, ctx, song):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        results = await player.node.get_tracks(song)
        track = results['tracks'][0]
        await self.player_song(ctx, track)

    @commands.command(aliases=['auto'])
    async def autoplay(self, ctx):
        future = asyncio.ensure_future(self.looped_task(ctx))
        _guild_autoloop = self.guild_autoplay[ctx.guild.id]
        print(_guild_autoloop)
        if _guild_autoloop is False:
            self.guild_autoplay.update({ctx.guild.id : True})
            print(_guild_autoloop)

        else:
            self.guild_autoplay.update({ctx.guild.id : False})
            future.cancel()
        #reverses the condition idk why?
        await ctx.send(' :robot: | Autoplay : ' + ('disabled' if _guild_autoloop is True else 'enabled'))

    async def looped_task(self, ctx):
        _guild_autoloop = self.guild_autoplay[ctx.guild.id]
        while _guild_autoloop:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            if len(player.queue) == 0:
                songs  = autoplay.get_yt(player.current.uri)
                for song in songs:
                    try:
                        await self.capture_track(ctx, song)
                    except Exception as e:
                        print(e)
                        continue
            await asyncio.sleep(4)

def setup(bot):
    bot.add_cog(Music_base(bot))