import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix = '=')
load_dotenv('.env')
@client.event
async def on_ready():
	print('bot is running')
@client.command(name = 'hello')
async def hello(ctx):
	await ctx.send('hello')
client.load_extension('cogs.sound')
client.load_extension('cogs.emotion')

client.run(os.getenv('token'))