from os import getenv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class discord_config:
    prefix = "$"
    token = getenv('token')
    yt_key = getenv('yt_key')
    music_queue_item = 10


class base_server_config:
    __version__ = "2.15"
    #lavaplayer configs 
    password = getenv('password')
    country = getenv('country')
    type_node = getenv('type_node')
    resume_key = None
    resume_timeout = 60
    name = None
    reconnect_times = 10
    ssl=False


