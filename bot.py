import os, sys, json, glob
import subprocess
import platform
import discord
import youtube_dl 
from discord.ext import commands 
from discord.utils import get 
from dotenv import load_dotenv 
from youtube_search import YoutubeSearch
from spotdl import __main__ as spotdl 
from tinytag import TinyTag

load_dotenv()

TOKEN = os.getenv('discord_token')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

##<Music stuff>##

youtube_dl.utils.bug_reports_message = lambda:''

ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' 
        #bind to ipv4 since ipv6 addresses cause issues sometimes
        }

ffmpeg_options = {
        'options': '-vn'
        }

songs = []

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volumen=0.5):
        super().__init__(source, volumen) 
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() 
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) ##?
        if 'entries' in data:
            # take first item from playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data) 
        return filename

def extract_info(track):
    info = ('0', '0')
    if not ('youtube.com' in track or 'youtu.be' in track):
        yt = YoutubeSearch(track, max_results=1).to_json()
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        url = 'https://www.youtube.com/watch?v=' + yt_id
        full_name = youtube_dl.YoutubeDL(ytdl_format_options).extract_info(url, download=False).get('title', None)
        info = (url, full_name) 
    else:
        full_name = youtube_dl.YoutubeDL(ytdl_format_options).extract_info(track, download=False).get('title', None)
        info = (track, full_name)
    return info

def mkLowerCase(value):
    lst_value = list(value)
    lwr = [x.lower() for x in lst_value]
    for i in range(len(lwr)):
        if lwr[i] == '_':
            lwr[i] = ' '
    res = ''
    for x in lwr:
        res += x
    return res 

def mp3_files(value): 
    all_the_files = os.listdir('./')
    mp3 = ''
    lwr_value = mkLowerCase(value)
    for file in all_the_files:
        lwr_file = mkLowerCase(file)
        if '.mp3' in file and lwr_value in lwr_file:
            mp3 = file
    return mp3

def mp3_info(file_path):
    tag = TinyTag.get(file_path)
    return (tag.title, tag.artist)

def first_track(values, f):
    res = -1
    for x in values:
        if x[1] == f:
            res = values.index(x)
            break
    return res 

# def queue(values, f):
#     i = 0
#     for x in values:
#         if x[1] == f:
#             i += 1
#     return (i == 0 and first_track(values, f) >= 0)

##</Music stuff>##

##<Debugging Commands>##

@bot.command(name='test', description='Makes a test text')
async def test(ctx):
    await ctx.send('This is a test so its my duty to say Hello World!')

@bot.command(name='playing_', description='Debugging tool to know if bot is playing something')
async def playing_(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await ctx.send("It's playing something")
    else:
        await ctx.send("It's doing nothing")

@bot.command(name='argument', description='Send a simple text')
async def argument(ctx, *, args):
    await ctx.send(args)

@bot.command(name='raw', description='Send the raw list')
async def raw(ctx):
    await ctx.send(songs)

##</Debugging Commands>##

##<Commands>##

@bot.command(name="join", description='Tells the bot to join the voice channel')
async def join(ctx):
    try:
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
    except discord.errors.ClientException:
        pass

@bot.command(name='leave', description='To make the bot leave the voice channel and erase junk')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

    path = os.getcwd()
    
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        files1 = glob.glob(path+'/*.m4a')
        files2 = glob.glob(path+'/*.webm')
        files3 = glob.glob(path+'/*.mp3')
    else:
        files1 = glob.glob(path+'\*.m4a')
        files2 = glob.glob(path+'\*.webm')
        files3 = glob.glob(path+'\*.mp3')
    
    for i in files1:
        try:
            os.unlink(i)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    for j in files2:
        try:
            os.unlink(j)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    for k in files3:
        try:
            os.unlink(k)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

@bot.command(name='play', description='To play song')
# async def play(ctx, f='y', *, value):
async def play(ctx, f='y', *, value):
    await join(ctx)
    if f == 'y':
        info = extract_info(value)

        def keep_rolling():
            # if len(songs_yt) != 0:
            if len(songs) != 0:
                voice = get(bot.voice_clients, guild=ctx.guild)
                filename = songs[first_track(songs, f)]
                songs.pop(first_track(songs, f))
                voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n : keep_rolling())

        try:
            server = ctx.message.guild
            voice_channel = server.voice_client 
            if not voice_channel.is_playing():
                async with ctx.typing():
                    voice = get(bot.voice_clients, guild=ctx.guild)
                    print('===Downloading {}==='.format(info[1]))
                    filename = await YTDLSource.from_url(info[0], loop=bot.loop)
                    print('===Done===')
                    voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n: keep_rolling())
                if info[1] != '0':
                    embed = discord.Embed(
                            title='**Now playing:**',
                            description=info[1],
                            color=discord.Color.green()
                            )
                    await ctx.send(embed=embed)
            else:
                print('===Downloading {}==='.format(info[1]))
                filename = await YTDLSource.from_url(info[0], loop=bot.loop)
                print('===Done===')
                track = (filename, f)
                songs.append(track)
                # songs_yt.append(filename)
                embed = discord.Embed(
                        title='Queue:',
                        description='{} was queued to the list'.format(info[1]),
                        color=discord.Color.greyple()
                        )
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                    title='Error!',
                    description='The bot has found an error!',
                    color=discord.Color.dark_red()
                    )
            await ctx.send(embed=embed)
    elif f == 's':
        def keep_spot_rolling():
            # if len(songs_spot) != 0:
            if len(songs) != 0:
                temp = first_track(songs, f)[0]
                voice = get(bot.voice_clients, guild=ctx.guild)
                subprocess.check_call([sys.executable, spotdl.__file__, temp])
                filename = mp3_files(songs[temp])
                songs.pop(temp)
                voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n : keep_spot_rolling())

        try:
            server = ctx.message.guild
            voice_client = server.voice_client 
            if not voice_client.is_playing():
                async with ctx.typing():
                    try:
                        subprocess.check_call([sys.executable, spotdl.__file__, value])
                        voice = get(bot.voice_clients, guild=ctx.guild)
                        filename = mp3_files(value)
                        voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n : keep_spot_rolling())
                    except:
                        pass
                        voice = get(bot.voice_clients, guild=ctx.guild)
                        filename = mp3_files(value)
                        voice_client.play(discord.FFmpegPCMAudio(source=filename))
                info = mp3_info(os.getcwd()+'/'+mp3_files(value))
                embed = discord.Embed(
                        title='**Now playing:**',
                        description='{0} by {1}'.format(info[0], info[1]),
                        color=discord.Color.green()
                        )
                await ctx.send(embed=embed)
                # os.unlink(os.getcwd()+'/'+mp3_files()[0])
            else:
                track = (value, f)
                songs.append(track)
                embed = discord.Embed(
                        title='Queue:',
                        description='{} was queued to the list'.format(value),
                        color=discord.Color.greyple()
                    )
                await ctx.send(embed=embed)
        except discord.errors.ClientException as e:
            embed = discord.Embed(
                    title='Error: {}!'.format(e),
                    description='The bot has found an error!',
                    color=discord.Color.dark_red()
                    )
            await ctx.send(embed=embed)

@bot.command(name='pause', description='Pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        embed = discord.Embed(
                title='Pause song',
                # description='{} was paused'.format(songs[0][0]),
                color=discord.Color.dark_gold()
                )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
                    title='Error!',
                    description='The bot is not playing anything at the moment',
                    color=discord.Color.dark_red()
                    )
        await ctx.send(embed=embed)

@bot.command(name='skip', description='Plays the next song of the playlist')
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        embed = discord.Embed(
                title='Skip song',
                # description='{} was skipped'.format(songs[0][0]),
                color=discord.Color.purple()
                )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
                title='Error!',
                description='The bot was not playing anything at the moment',
                color=discord.Color.dark_red()
                )
        await ctx.send(embed=embed)

@bot.command(name='resume', description='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        embed = discord.Embed(
                title='Resume music',
                # description='Continue playing {}'.format(songs[0][0]),
                color=discord.Color.green()
                )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
                title='Error!',
                description='The bot was not playing anything at the moment',
                color=discord.Color.dark_red()
                )
        await ctx.send(embed=embed)

@bot.command(name='remove', description='Delete the nth queued song')
async def remove(ctx, n: int):
    temp = ''
    # if songs[n][1] == f:
    temp = songs[n][0]
    songs.pop(n)
    embed = discord.Embed(
            title='Song deleted',
            description='{} was deleted'.format(temp),
            color=discord.Color.dark_blue()
            )
    await ctx.send(embed=embed)

@bot.command(name='playlist', description='To see the queued songs')
async def playlist(ctx):
    infoPlay = """ 
    
    """    
    for i in range(len(songs)):
        infoPlay += '**[' + str(i) + ']**' + '**[' + '{}' + ']**' + """ = {},\n"""
        
    infoPlay = infoPlay.format(*songs[1], *songs[0])
        
    embed = discord.Embed(
            title='Playlist',
            description=infoPlay,
            color=discord.Color.blue()
            )
        
    await ctx.send(embed=embed)

@bot.command(name='commands', description='Display the commands')
async def commands(ctx):
    des = """
    Commands of VinylBot, Prefix: $, f: Y/s (youtube/spotify)\n

    > join: Tells the bot to join the voice channel

    > leave: To make the bot leave the voice channel and erase junk

    > play f url/name: To play song   

    > playlist: To see the queued songs 

    > pause: Pauses the song

    > skip: Stop songs and plays the next one if there's a playlist

    > resume: Resumes the song

    > remove n: Delete the nth song from the queue 

    > commands: Display the commands\n

    Made with love and Python\n

    Source Code: https://github.com/martinykrz/VinylBot 

    """
    embed = discord.Embed(
                title="I'm VinylBot, A Music Bot", 
                description=des, 
                color=discord.Color.blue()
                )

    await ctx.send(embed=embed)

##</Commands>##

bot.run(TOKEN)
