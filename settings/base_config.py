from os import getenv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class discord_config:
    prefix = "$"
    token = getenv('token')
    yt_api_key = getenv('yt_api_token')
    music_queue_item = 5


class base_server_config:
    #lavaplayer configs 
    password = getenv('password')
    country = getenv('country')
    type_node = getenv('type_node')
    resume_key = None
    resume_timeout = 60
    name = None
    reconnect_times = 10
    ssl=False


