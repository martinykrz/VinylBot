#!/usr/bin/env python
import os
import json
import yt_dlp
import asyncio
import discord
import traceback
import dotenv
import argparse
from sys import platform
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from gtts import gTTS
from youtube_search import YoutubeSearch
from ytmusicapi import YTMusic
from spotdl.utils.spotify import SpotifyClient
from spotdl.types.song import Song

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category='Commands', show_parameters_description=True)

bot = commands.Bot(
        command_prefix='-', 
        case_insensitive=True, 
        intents=intents,
        help_command=help_command
        )

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

##<Music stuff>##

class Music:
    def __init__(self):
        self.song = ''
        self.name = ''
        self.author = ''
        self.path = "{}/Music/".format(os.path.expanduser("~"))
        self.exit = False
        #Spotify Client
        client_id = 'adfb10751507481fbd3d75b2b1c36d9e'
        client_secret = 'ac72e6687cd84568801bfe9c6709aa33'
        
        SpotifyClient.init(client_id, client_secret, False)
        
        self.ytmusic = YTMusic()
        
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
            'source_address': '0.0.0.0', #bind to ipv4 since ipv6 addresses cause issues sometimes
        }
        
        # Quiet yt-dlp
        yt_dlp.utils.bug_reports_message = lambda:''
        
        self.ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
    
    def nameFilter(self):
        if 'spotify' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' spotify'))]
        elif 'local' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' local'))]
        elif 'playlist' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' playlist'))]

    def normalSong(self):
        if 'local' in self.song:
            self.nameFilter()
        else:
            yt = YoutubeSearch(self.song, max_results=1).to_json()
            self.song = 'https://www.youtube.com/watch?v=' + str(json.loads(yt)['videos'][0]['id'])
            self.name = self.ytdl.extract_info(self.song, download=False).get('title', None)
            self.author = str(json.loads(yt)['videos'][0]['channel'])

    def spotifySong(self):
        if 'track' in self.song:
            self.name = Song.from_url(self.song).name
            self.song = 'https://www.youtube.com/watch?v=' + ytmusic.search(self.name, 'songs')[0]['videoId']
            self.author = self.ytmusic.search(title, 'songs')[0]['artists'][0]['name']
        else:
            self.nameFilter()
            
            ytm = self.ytmusic.search(self.song, 'songs')[0]
            self.song = 'https://www.youtube.com/watch?v=' + ytm['videoId']
            self.name = ytm['title']
            self.author = ytm['artists'][0]['name']

    def urlSong(self):
        self.name = self.ytdl.extract_info(self.song, download=False).get('title', None)
        self.author = str(json.loads(YoutubeSearch(self.name, max_results=1).to_json())['videos'][0]['channel'])

    def makeTrack(self):
        if 'spotify' in self.song:
            self.spotifySong()
        elif 'youtube.com' in self.song or 'youtu.be' in self.song:
            self.urlSong()
        else:
            self.normalSong()

    def songData(self, song):
        self.song = song
        self.makeTrack()
        return self.song, self.name, self.author

music = Music()

ffmpeg_options = {
        'options': '-vn'
        }

songs = []

# Search and download music
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volumen=0.5):
        super().__init__(source, volumen) 
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() 
        data = await loop.run_in_executor(None, lambda: music.ytdl.extract_info(url, download=not stream)) 
        
        if 'entries' in data:
            # take first item from playlist
            data = data['entries'][0]
        
        filename = data['title'] if stream else music.ytdl.prepare_filename(data) 
        
        if platform != "win32":
            os.system(f"mv {filename} /tmp/{filename}")
            filename = f"/tmp/{filename}"
        else:
            if not os.path.exists("songs"):
                os.mkdir("songs")
            
            os.system(f"move {filename} songs\\{filename}")
            filename = f"songs\\{filename}"
        return filename

##</Music stuff>##

##<Debugging Commands>##

@bot.command(name='test', description='Makes a test text', hidden=True)
async def test(ctx):
    await ctx.send('This is a test so its my duty to say Hello World!')

@bot.command(name='playing_', description='Debugging tool to know if bot is playing something', hidden=True)
async def playing_(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await ctx.send("It's playing something")
    else:
        await ctx.send("It's doing nothing")

@bot.command(name='arg', description='Send a simple text', hidden=True)
async def arg(ctx, *, args):
    embed = discord.Embed(
            description='This is a test, {}'.format(args)
            )
    await ctx.send(embed=embed)

@bot.command(name='raw', description='Send the raw list', hidden=True)
async def raw(ctx):
    await ctx.send(songs)

@bot.command(name='f', description='Send a text file', hidden=True)
async def file(ctx, *, args):
    file = discord.File(args)
    await ctx.send(file=file)

@bot.command(name='debug', description='Show debug commands', hidden=True)
async def debug(ctx):
    des = f"""
    Debug commands of {bot.user.name}, Prefix: -\n

    > test: Sends a fixed message

    > playing_: Check if it's playing something

    > arg text: Sends a custom message

    > raw: View filename of the queued songs

    > file path/to/file: Sends a file 

    > debug: Display the debug commands\n

    """
    embed = discord.Embed(
                title=f"I'm {bot.user.name}, A Music Bot", 
                description=des, 
                color=discord.Color.blue()
                )

    await ctx.send(embed=embed)

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

@bot.command(name='leave', description='Bot leaves the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
    
    if platform == "win32":
        for root, _, files in os.walk("songs", topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                while True:
                    try:
                        os.remove(file_path)
                        break
                    except:
                        continue
        
        os.rmdir("songs")

@bot.command(name='play', description='Plays song', aliases=["p"])
async def play(ctx, *, value: str = commands.parameter(description="URL, Name, Name + spotify")):
    await join(ctx)
    track = music.songData(value)

    def keep_rolling():
        if len(songs) != 0:
            voice = get(bot.voice_clients, guild=ctx.guild)
            channel = get(ctx.guild.text_channels, name=ctx.message.channel.name)
            file = songs[0]
            songs.pop(0)
            embed = discord.Embed(
                        title='**Now playing:**',
                        description='{} by {}'.format(file[1], file[2]),
                        color=discord.Color.green()
                        )
            coro = channel.send(embed=embed)
            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
            
            try:
                fut.result()
            except:
                pass
            
            voice.play(discord.FFmpegPCMAudio(source=file[0]), after=lambda n : keep_rolling())

    try:
        server = ctx.message.guild
        voice_channel = server.voice_client 
        if not voice_channel.is_playing():
            async with ctx.typing():
                voice = get(bot.voice_clients, guild=ctx.guild)
                file = await YTDLSource.from_url(track[0], loop=bot.loop)
                voice.play(discord.FFmpegPCMAudio(source=file), after=lambda n: keep_rolling())
            if track[1] != '0':
                embed = discord.Embed(
                        title='**Now playing:**',
                        description='{} by {}'.format(track[1], track[2]),
                        color=discord.Color.green()
                        )
                await ctx.send(embed=embed)
        else:
            file = await YTDLSource.from_url(track[0], loop=bot.loop)
            songs.append((file, track[1], track[2]))
            embed = discord.Embed(
                    title='Queue:',
                    description='{} was queued to the list'.format(track[1]),
                    color=discord.Color.greyple()
                    )
            await ctx.send(embed=embed)
    except Exception as exp:
        print(traceback.format_exc())
        embed = discord.Embed(
                title='Error!',
                description=f'{exp}',
                color=discord.Color.dark_red()
                )
        await ctx.send(embed=embed)

@bot.command(name='local', description='Plays local audio files')
async def local(ctx, *, value: str = commands.parameter(description=".mp3, .mp4, .mkv")):
    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    filename = value
    voice.play(discord.FFmpegPCMAudio(source=filename))

@bot.command(name='tts', description='Text To Speech')
async def TTS(ctx, *, value: str):
    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    author = ctx.author
    tts = gTTS(f"{author.global_name} dice: {value}", lang="es")
    filename = f"/tmp/{value.replace(' ', '_')}.mp3" if platform != "win32" else f"songs\\{value.replace(' ', '_')}.mp3"
    tts.save(filename)
    voice.play(discord.FFmpegPCMAudio(filename))

@bot.command(name="song", description='Changes the status of the song', hidden=True)
async def song(ctx, value : str):
    voice_client = ctx.message.guild.voice_client
    txt: str = ''
    des: str = ''
    color = discord.Color
    if voice_client.is_playing():
        match value:
            case 'p':
                voice_client.pause()
                txt = "Pause song"
                color = color.dark_gold()
            case 's':
                voice_client.stop()
                txt = "Skip song"
                color = color.purple()
            case _:
                txt = "Error: No arguments sended"
                color = color.dark_red()
    elif voice_client.is_paused():
        match value:
            case 'r':
                voice_client.resume()
                txt = "Resume song"
                color = color.green()
            case _:
                txt = "Error: No arguments sended"
                color = color.dark_red()
    else:
        txt = "Error!"
        color = color.dark_red()
        des = "The bot is not playing anything at the moment" 
    embed = discord.Embed(
            title=txt,
            description=des,
            color=color
            )
    await ctx.send(embed=embed)

@bot.command(name='pause', description='Pauses the song')
async def pause(ctx):
    await song(ctx, 'p')

@bot.command(name='skip', description='Skips the current song')
async def skip(ctx):
    await song(ctx, 's')

@bot.command(name='resume', description='Resumes the song')
async def resume(ctx):
    await song(ctx, 'r')

@bot.command(name='queue', description='View Queued songs')
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

##</Commands>##

parser = argparse.ArgumentParser()
parser.add_argument("token", type=str)
args = parser.parse_args()
token: str = f"TOKEN_{args.token.upper()}"

async def main():
    try:
        await bot.start(os.getenv(token))
    except asyncio.CancelledError:
        return None

asyncio.run(main())
