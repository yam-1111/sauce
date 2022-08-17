
from .base_config import base_server_config
from os import getenv
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class standalone_lavaplayer(base_server_config):
    node = "127.0.0.1"
    host = "localhost"
    port = 2333

class web_server(base_server_config):
    node = getenv('web_node')
    host = getenv('web_host')
    port = int(getenv('web_port'))

class heroku_server(base_server_config):
    node = getenv('heroku_node')
    host = getenv('heroku_host')
    port= int(getenv('heroku_port'))

class repl_server(base_server_config):
    """Applicable only on lavalink4.0 on github version"""
    node = getenv('repl_node')
    host = getenv('repl_host')
    port = int(getenv('repl_port'))
    ssl= bool(getenv('repl_ssl'))

def launcher(server_type='web'):
    if server_type == 'local':
        return standalone_lavaplayer
    elif server_type == 'web':
        return web_server
    elif server_type == 'heroku':
        return heroku_server
    elif server_type == 'repl':
        return repl_server

