import re
import urllib.request
import requests
import random
from datetime import datetime
from settings.base_config import discord_config as command

class ui:
    yt = "https://img.icons8.com/external-those-icons-lineal-color-those-icons/24/000000/external-youtube-applications-windows-those-icons-lineal-color-those-icons.png"
    queue_icon = "https://cdn-icons-png.flaticon.com/512/1282/1282648.png"


class color:
    fuchsia = 0xD9027D
    purple = 0xA921E8
    orange = 0xFDA326
    green = 0x27E024
    red = 0xF40B5D
    yellow = 0xffe74d
    pink = 0xfc38ff


class photos:
    def thumbnail(uri):
        img = re.findall(r"watch\?v=(\S{11})", uri)
        return f"http://i.ytimg.com/vi/{img[0]}/hqdefault.jpg"

    def icon(uri):
        html = urllib.request.urlopen(uri)
        author_image = re.search(r'yt3\.ggpht\.com/[^"]+', html.read().decode())
        if author_image:
            return f"https://{author_image.group()}"
        return None


class mechanism:
    def get_time():
        """Returns the current time"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time
        
    def get_yt(data):
        html = urllib.request.urlopen(data)
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        num = random.sample(range(16, len(video_ids)), 1)
        for numbers in num:
            data = numbers

    def ms_duration(ms : int, is_live : bool):
        if not is_live:
            sec = (ms/1000)%60
            min = ((ms/(1000*60))% 60)
            hr = (ms / (1000*60*60))%24
            print(hr, min, sec)
            if hr <= 1:
                return ("%02d:%02d" % (min, sec))
                if min <= 1:    
                    return ("0:%d" %(min, sec))
            return ("%d:%02d:%02d" % (hr, min, sec))
        return 'Live'
class autoplay:
    def get_yt(data, num :int=20):
        lst = []
        orig_uri = re.findall(r'watch\?v=(\S{11})', data)
        url = f"https://www.googleapis.com/youtube/v3/search?key={command.yt_key}&maxResults={num}&part=snippet&type=video&relatedToVideoId={orig_uri[0]}"
        result = requests.get(url).json()
        for n, x in enumerate(result):
            try:
                uri = (result['items'][n]['id']['videoId'])
                lst.append(uri)
            except IndexError:
                pass
        return lst