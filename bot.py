import os, sys, json, glob
import subprocess
import asyncio
import platform
import discord
import yt_dlp
from discord.ext import commands 
from discord.utils import get 
from dotenv import load_dotenv 
from youtube_search import YoutubeSearch
from spotdl.search import SpotifyClient  
from spotdl.providers.metadata_provider import from_url as spotInfo
from ytmusicapi import YTMusic

load_dotenv()

TOKEN = os.getenv('discord_token')

CLIENT_ID = os.getenv('client_id')

CLIENT_SECRET = os.getenv('client_secret')

SpotifyClient.init(CLIENT_ID, CLIENT_SECRET, False)

ytmusic = YTMusic()

bot = commands.Bot(command_prefix='-', case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

##<Music stuff>##

yt_dlp.utils.bug_reports_message = lambda:''

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

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volumen=0.5):
        super().__init__(source, volumen) 
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() 
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) 
        if 'entries' in data:
            # take first item from playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data) 
        return filename

def filter_name_noise(track):
    f = len(list('spotify'))
    sample = list(track)
    res = 0
    for i in range(len(sample)):
        tmp = ''
        for j in range(i, f+i):
            tmp += sample[j]
        if tmp == 'spotify':
            res = i
            break
    if res != 0:
        while res < len(sample):
            sample.pop(res)
    else:
        while res <= f:
            sample.pop(0)
            res += 1
    result = ''
    for k in range(len(sample)):
        result += sample[k]
    return result

def extractName(filename):
    temp = list(filename)
    r = []
    if '.m4a' in filename:
        for i in range(0, len(temp)-4):
            r.append(temp[i])
    elif '.webm' in filename:
        for j in range(0, len(temp)-5):
            r.append(temp[j])
    res = ''
    for k in range(len(r)-11):
        res += r[k]
    return res

def make_Info(track):
    info = ('0', '0', '0')
    if not ('youtube.com' in track or 'youtu.be' in track):
        if 'spotify' in track and not 'open.' in track:
            track = filter_name_noise(track)
            print('===Downloading from Spotify===')
            ytm = ytmusic.search(track, 'songs')[0]
            ytm_id = ytm['videoId']
            title = ytm['title']
            artist = ytm['artists'][0]['name']
            url = 'https://www.youtube.com/watch?v=' + ytm_id
            info = (url, title, artist)
        else:
            yt = YoutubeSearch(track, max_results=1).to_json()
            yt_id = str(json.loads(yt)['videos'][0]['id'])
            yt_artist = str(json.loads(yt)['videos'][0]['channel'])
            url = 'https://www.youtube.com/watch?v=' + yt_id
            full_name = ytdl.extract_info(url, download=False).get('title', None)
            info = (url, full_name, yt_artist) 
    elif 'open.spotify.com' in track and 'track' in track:
        title = spotInfo(track)[0]["name"] #First item from the search
        ytm_id = ytmusic.search(title, 'songs')[0]['videoId']
        ytm_artist = ytmusic.search(title, 'songs')[0]['artists'][0]['name']
        url = 'https://www.youtube.com/watch?v=' + ytm_id
        info = (url, title, ytm_artist)
    else:
        full_name = ytdl.extract_info(track, download=False).get('title', None)
        yt = YoutubeSearch(track, max_results=1).to_json()
        artist = str(json.loads(yt)['videos'][0]['channel'])
        info = (track, full_name, artist)
    return info

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

@bot.command(name='arg', description='Send a simple text')
async def arg(ctx, *, args):
    embed = discord.Embed(
            description='This is a test, {}'.format(args)
            )
    await ctx.send(embed=embed)

@bot.command(name='raw', description='Send the raw list')
async def raw(ctx):
    await ctx.send(songs)

@bot.command(name='f', description='Send a text file')
async def file(ctx, *, args):
    file = discord.File(args)
    await ctx.send(file=file)

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
    else:
        files1 = glob.glob(path+'\*.m4a')
        files2 = glob.glob(path+'\*.webm')
    
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

@bot.command(name='p', description='To play song from Youtube')
async def play(ctx, *, value):
    await join(ctx)
    info = make_Info(value)

    def keep_rolling():
        if len(songs) != 0:
            voice = get(bot.voice_clients, guild=ctx.guild)
            channel = get(ctx.guild.text_channels, name=ctx.message.channel.name)
            filename = songs[0]
            songs.pop(0)
            file_title= extractName(filename)
            # url = 'https://www.youtube.com/watch?v=' + file_id
            info = make_Info(file_title)
            embed = discord.Embed(
                        title='**Now playing:**',
                        description='{} by {}'.format(info[1], info[2]),
                        color=discord.Color.green()
                        )
            coro = channel.send(embed=embed)
            # coro = channel.send(filename)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            try:
                fut.result()
            except:
                pass
            voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n : keep_rolling())

    try:
        server = ctx.message.guild
        voice_channel = server.voice_client 
        if not voice_channel.is_playing():
            async with ctx.typing():
                voice = get(bot.voice_clients, guild=ctx.guild)
                print('===Downloading {}==='.format(info[1]))
                timer = time.time() 
                filename = await YTDLSource.from_url(info[0], loop=bot.loop)
                print('===Done in {} s==='.format(round(time.time()-timer, 2)))
                voice.play(discord.FFmpegPCMAudio(source=filename), after=lambda n: keep_rolling())
            if info[1] != '0':
                embed = discord.Embed(
                        title='**Now playing:**',
                        description='{} by {}'.format(info[1], info[2]),
                        color=discord.Color.green()
                        )
                await ctx.send(embed=embed)
        else:
            print('===Downloading {}==='.format(info[1]))
            timer = time.time()
            filename = await YTDLSource.from_url(info[0], loop=bot.loop)
            print('===Done in {} s==='.format(round(time.time() - timer, 2)))
            songs.append(filename)
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

@bot.command(name='pause', description='Pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        embed = discord.Embed(
                title='Pause song',
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
    temp = songs[n]
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
        infoPlay += '**[' + str(i) + ']**' + """ = {},\n"""
        
    infoPlay = infoPlay.format(*songs)
        
    embed = discord.Embed(
            title='Playlist',
            description=infoPlay,
            color=discord.Color.blue()
            )
        
    await ctx.send(embed=embed)

@bot.command(name='commands', description='Display the commands')
async def commands(ctx):
    des = """
    Commands of VinylBot, Prefix: -\n

    > join: Tells the bot to join the voice channel

    > leave: To make the bot leave the voice channel and erase junk

    > (p)lay url/name: To play song (add 'spotify' to search from Spotify) 

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

