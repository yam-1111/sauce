
from discord.ext import commands
import discord
import lavalink
import math
from utils.interface import * 
from settings.base_config import discord_config

class Music_queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_base = self.bot.get_cog('Music_base')

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        local_queue = self.music_base.guild_queue_detail[ctx.guild.id]
        items_per_page = discord_config.music_queue_item
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
       
        pages = math.ceil(len(local_queue) / items_per_page)
        print(pages)
        if page > pages:
            embed = discord.Embed(title=" :warning: You've reach the limit", colour=color.yellow)   
        else:
            start = (page - 1) * items_per_page
            end = start + items_per_page
            if len(player.queue) is None:
                queue_list = 'No queue yet'
            else:
                queue_list = ''
                for x,track in enumerate(self.music_base.guild_queue_detail[ctx.guild.id][start:end], start=start):
                    queue_list += f'{x + 1}) { "[Now Playing]" if player.current.title == track[0] else mechanism.ms_duration(track[1], track[2])} >> {track[0][:29]+".." if len(track[0]) > 29 else track[0]} \n'

            print(queue_list)
            embed = discord.Embed(colour=color.green, 
            title=player.current.title[:45] + "..."if len(player.current.title)>45 else player.current.title,
             url=player.current.uri)


            embed.add_field(value=f"```{'='*9} {len(player.queue)} tracks queued {'='*10}\n{queue_list}\n{'='*13} page {page} / {pages} {'='*13}```"
            , 
            name=f'{mechanism.ms_duration(player.current.duration, player.current.stream)} {await self.music_base.player_system_interface(ctx)}'
            )
            embed.set_thumbnail(url=photos.thumbnail(player.current.uri))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music_queue(bot))