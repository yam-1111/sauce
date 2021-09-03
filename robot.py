import discord
from discord.ext import commands
import asyncio
from cogs.sound import Sound

token = 'your_token'
client = commands.Bot(command_prefix='$')
@client.event
async def on_ready():
    print('status online')
async def setup():
    await client.wait_until_ready()
    client.add_cog(Sound(client))
client.load_extension('cogs.about')
client.load_extension('cogs.covid')

client.loop.create_task(setup())
client.run(token)
