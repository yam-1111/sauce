from discord.ext import commands
import lavalink
import discord

class Test_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_base = self.bot.get_cog('Music_base')

    @commands.command()
    async def test(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        print(self.music_base.guild_queue_detail)
        print(self.music_base.guild_queues[ctx.guild.id].index(player.current.uri))
def setup(bot):
    bot.add_cog(Test_module(bot))
