import os, json, glob
import platform
import discord
import youtube_dl 
from discord.ext import commands,tasks 
from dotenv import load_dotenv 
from youtube_search import YoutubeSearch

load_dotenv()

TOKEN = os.getenv('discord_token')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

##Music stuff##

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
        super().__init__(source, volumen) ##??
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() ##??
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) ##?
        if 'entries' in data:
            # take first item from playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data) ##??
        return filename

def title_to_url(track):
    yt = YoutubeSearch(track, max_results=1).to_json()
    try:
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        url = 'https://www.youtube.com/watch?v=' + yt_id
        full_name = youtube_dl.YoutubeDL(ytdl_format_options).extract_info(url, download=False).get('title', None)
        return (url, full_name) 
    except:
        pass
        return ('0', '0')

def url_to_title(url):
    try:
        full_name = youtube_dl.YoutubeDL(ytdl_format_options).extract_info(url, download=False).get('title', None)
        return (url, full_name)
    except:
        pass 
        return ('0', '0')

def is_url(value):
    standard = list('https://')
    test = list(value)
    while len(test) < len(standard):
        test.append(" ")
    n = 0
    for i in range(len(standard)):
        if standard[i] == test[i]:
            n += 1
    return n == len(standard)

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

##</Debugging Commands>##

##<Commands>##

@bot.command(name="join", description='Tells the bot to join the voice channel')
async def join(ctx):
    try:
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            # return
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
    
    if platform.system() == 'Linux':
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

@bot.command(name='play', description='To play song')
async def play(ctx, value):
    await join(ctx)
    if is_url(value):
        name = url_to_title(value)
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client    
            if not voice_channel.is_playing():
                async with ctx.typing():
                    filename = await YTDLSource.from_url(name[0], loop=bot.loop)
                    voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
                if name[1] != '0':
                    await ctx.send('**Now playing:** {}'.format(name[1]))
            else:
                songs.append(value)
                await ctx.send('{} was queued to the list'.format(name[1]))
        except:
            await ctx.send("The bot has found an error!") 
    else:
        url = title_to_url(value)
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client 
            if not voice_channel.is_playing():
                async with ctx.typing():
                    if url[0] != '0':
                        filename = await YTDLSource.from_url(url[0], loop=bot.loop)
                        voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
                    else:
                        raise ValueError
                if url[1] != '0':
                    await ctx.send('**Now playing:** {}'.format(url[1]))
            else:
                songs.append(value)
                await ctx.send('{} was queued to the list'.format(url[1]))
        except:
            await ctx.send("The bot has found an error!") 

@bot.command(name='playlist', description='To see the queued songs')
async def playlist(ctx):
    await ctx.send(songs)

@bot.command(name='pause', description='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Pause music.")
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='skip', description='Skip to the nth queued song')
async def skip(ctx, n: int):
    voice_client = ctx.message.guild.voice_client 
    if len(songs) > 0 or voice_client.is_playing():
        voice_client.stop()
        try:
            await play(ctx, songs[n])
            songs.pop(n)
        except:
            await ctx.send("The bot found an error!")

@bot.command(name='next', description='Plays the next song of the playlist')
async def next(ctx):
    await skip(ctx, 0)

@bot.command(name='resume', description='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resume music.")
    else:
        await ctx.send("The bot was not playing anything at the moment.")

@bot.command(name='stop', description='Stops the current song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Stop music.")
    elif len(songs) > 0:
        await play(ctx, songs[0])
        songs.pop(0)
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='commands', description='Display the commands')
async def commands(ctx):
    des = """
    Commands of B.O.T, Prefix: $\n

    > join: Tells the bot to join the voice channel

    > leave: To make the bot leave the voice channel and erase junk

    > play: To play song

    > playlist: To see the queued songs

    > pause: This command pauses the song

    > skip n: Skip to the nth queued song

    > next: Plays the next song of the playlist

    > resume: Resumes the song

    > stop: Stops the current song

    > commands: Display the commands\n

    Made with love and Python

    """
    embed = discord.Embed(
                title="I'm B.O.T, A SemiAutomatic Music Bot", 
                description=des, 
                color=discord.Color.random()
                )

    await ctx.send(embed=embed)

##</Commands>##

bot.run(TOKEN)

