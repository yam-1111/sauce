
from discord.ext import commands, tasks
import lavalink
import asyncio
import re
from utils.interface import color
url_rx = re.compile(r'https?://(?:www\.)?.+')
time_rx =re.compile('[0-9]+')

class Music_control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repeat_counter={}



    @commands.command()
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            await ctx.send(':x: No music to shuffle')
        player.shuffle = not player.shuffle
        await ctx.send('🔀 | song shuffling  ' + ('enabled' if player.shuffle else 'disabled'))

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | music resumed')
        else:
            await player.set_pause(True)
            await ctx.send(' ⏯ | music paused')
    
    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Nothing playing.')
        player.repeat = not player.repeat
        await ctx.send('🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled'))

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int=None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'🔈 >> {player.volume}%')
        await player.set_volume(volume)
        await ctx.send(f'🔈 || Set to {player.volume}%')
def setup(bot):
    bot.add_cog(Music_control(bot))