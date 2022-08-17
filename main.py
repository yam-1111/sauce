
import discord
import os
from discord.ext import commands, tasks
from settings.base_config import discord_config as command
# from router.routes import keep_run
from random import choice
from settings.config import keep_run

client = commands.Bot(command_prefix=command.prefix)

status = [
    f"{len(client.guilds)} guilds", f"at {command.prefix} command prefix",
    'Keep chilling...'
]
@client.event
async def on_ready():
    print(f"{'='*10} Online {'='*10}")
    import lavalink
    print(f'Lavalink Version : {lavalink.__version__}')
    print(f"{'='*20}")
    for cogs in os.listdir('./cogs'):
        if cogs.endswith('.py'):
            client.load_extension(f"cogs.{cogs[:-3]}")
            print(f"cogs.{cogs[:-3]} -- has been loaded")



@tasks.loop(seconds=20)
async def bot_status():
    
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=(choice(status))
        )
    )



client.run(command.token)