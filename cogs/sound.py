import pafy
import youtube_dl
import asyncio
from pytube import Playlist
import discord
from discord.ext import commands

class Sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        #if len(self.song_queue[ctx.guild.id]) > 0:
            #ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):   
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        
        ctx.voice_client.source.volume = 0.8
        await self.send_msg(ctx, song)
    async def send_msg(self, ctx, song):
        url2 = pafy.new(song)
        seconds = url2.length
        def next_song():
            try:
                temp_song = self.song_queue[ctx.guild.id][1]
                song = pafy.new(temp_song)
                return song.title
            except Exception as e:
                return 'no queue yet'
                print(e)
        def convert_timer(seconds):
            a = (seconds//3600)
            b=((seconds%3600)//60)
            c=((seconds%3600)%60)
            if a == 0:
                return '{:02d}:{:02d}'.format(b, c)
            else:
                return '{:02d}:{:02d}:{:02d}'.format(a, b, c)
        embed2 = discord.Embed(title= url2.title, url=song, color=0x843cdd)
        embed2.set_author(name='Now Playing: ')
        embed2.add_field(name=f':clock4: Duration:', value=convert_timer(seconds))
        embed2.set_thumbnail(url=url2.bigthumb)
       # embed2.description(text=f'{convert_timer(seconds)}')
        embed2.add_field(name=':musical_note: Next Song: ' ,value=next_song())
        embed2.set_footer(text=f'requested by: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed2)

        
        

    

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.send(':door:  i leave your channel and clear queue ')
                     
            self.song_queue[ctx.guild.id].clear() 
            return await ctx.voice_client.disconnect()
            

        await ctx.send("I am not connected to a voice channel.")
    @commands.command(name='p')
    async def play(self, ctx, *, song=None):
        if ctx.author.voice is None:
            await ctx.send('you are not in voice channel')
       
        if song is None:
            return await ctx.send("missing song argument.")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
       

        # handle song whether it is url, playlist or a keyword then if not throw none.
        if ('https://www.youtube.com/playlist' in song):
            playlist = Playlist(song)
            for video in playlist:
                self.song_queue[ctx.guild.id].append(video) 
            await ctx.send('playlist added to queue!')
                
        elif not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("fetching results...")

            result = await self.search_song(3, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[1]

        if ctx.voice_client.source is not None:
            global music
            music = pafy.new(song)
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 30:
                self.song_queue[ctx.guild.id].append(song)
                embed2 = discord.Embed(title='Next Song', color=0x843cdd)
                embed2.add_field(name=f':timer: Positioned at #{queue_len+1}', value= music.title)
                embed2.set_thumbnail(url=music.bigthumb)
                embed2.set_footer(text=f'requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed2)

            else:
                embed2 = discord.Embed(title=' :warning: Queue overload please wait to finish current song', color=discord.Colour.red())
                return await ctx.send(embed = embed2)

        await self.play_song(ctx, song)
      

    @commands.command(name='m')
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command(name='q')
    async def queue(self, ctx): # display the current guilds queue
        if ctx.author.voice is None:
            await ctx.send(":upside_down: you are not in voice channel")
        else:
            if len(self.song_queue[ctx.guild.id]) == 0:
                return await ctx.send("There are currently no songs in the queue.")

            embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.blurple())
            i = 1
            for song in self.song_queue[ctx.guild.id]:
                music=pafy.new(song)
                queue_sec = music.length
                # track recognition
                def convert_timer(seconds):
                    a = (seconds//3600)
                    b=((seconds%3600)//60)
                    c=((seconds%3600)%60)
                    if a == 0:
                        return '{:02d}:{:02d}'.format(b, c)
                    else:
                        return '{:02d}:{:02d}:{:02d}'.format(a, b, c)
                embed.description += f"{i}) {music.title} {convert_timer(queue_sec)}\n"

                i += 1

            embed.set_footer(text="tip: you can use #m to search tracks without playing")
            await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
      
            return await ctx.send("No songs in queue yet.")
            skip = False
        skip = True
       
        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)
    @commands.command()
    async def remove(self, ctx, amount: int=None):
        try:
            if amount is not None:
                amount -= 1
                self.song_queue[ctx.guild.id].pop(amount)
                await ctx.send('succefully remove song!')
                await self.queue(self, ctx)
            if amount is None:
                await ctx.send('please remove number based on queue, cant find? try **$q**')
        except Exception as e:
            print(e)
            await ctx.send('error, ')

      
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")
        
        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.") 
