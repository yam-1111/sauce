
from discord.ext import commands
import discord
version='0.3.1'
desc='not same as groovy but can play songs and monitor covid tolls all over the world'
purple=0x9130f3

class about(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('about succesfully loaded')
    @commands.command()
    async def about(self, ctx):
        embed2 = discord.Embed(title='sauce bot', color=purple)
        embed2.set_thumbnail(url="https://cdn.discordapp.com/app-icons/874571981712928809/819ff854244d8eecb20dcbabb24ffa23.png")
        embed2.add_field(name='version ', value=version)
        embed2.add_field(name='develop by' ,value='anthony john ')
        embed2.set_footer(text='this bot is currently on construction, not stable yet')
        await ctx.send(embed=embed2)



                
  




        
    
def setup(client):
    client.add_cog(about(client))
