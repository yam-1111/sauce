
"""
Edit this config file to run the server and the player itself
"""
from settings import server_config
from router.routes import keep_run

run_withplayer = False  #set to default False
service = 'local'


def bot_launcher(run_withplayer, service):
    if run_withplayer:
        keep_run(True)
        return server_config.launcher(service)
    else:
        keep_run()
        return server_config.launcher(service)

server = bot_launcher(run_withplayer, service)

