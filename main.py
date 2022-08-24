
import discord
import os
from discord.ext import commands, tasks
from settings.base_config import discord_config as command
from settings.base_config import base_server_config as bot_client
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
    print(f'Client version: {bot_client.__version__}\nLavalink Version : {lavalink.__version__} \nDiscord Version {discord.__version__}')
    print(f"{'='*29}")
    for cogs in os.listdir('./cogs'):
        if cogs.endswith('.py'):
            try:
                client.load_extension(f"cogs.{cogs[:-3]}")
            except Exception as e:
                print(f"{'='*10} Start of Error of cogs.{cogs[:-3]} {'='*10}")
                print(e)
                print(f"{'='*10} End of Error {'='*10}")
            print(f"cogs.{cogs[:-3]} -- has been loaded")
    print('/'*30)
    await bot_status()


@tasks.loop(seconds=20)
async def bot_status():
    
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=(choice(status))
        )
    )



client.run(command.token)