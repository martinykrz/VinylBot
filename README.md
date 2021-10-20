# VinylBot
Very basic music discord bot 

## Dependecies
1. Programs
    * python
    * pip
    * ffmpeg

2. Libraries
    * discord.py
    * python-dotenv
    * spotdl
    * yt-dlp
    * youtube-search

## Install the programs

### Windows 
* [Instructions to install ffmpeg on Windows and add it to PATH](https://windowsloop.com/install-ffmpeg-windows-10/)
* [Download the python executable and add it to PATH](https://www.python.org/downloads/)
* If you don't have pip installed, download this [file](https://bootstrap.pypa.io/get-pip.py) and type in cmd `python get-pip.py`

### Linux

#### Debian/Ubuntu
```
$ sudo apt update 
$ sudo apt install python3 ffmpeg python3-pip
```

### Fedora
``` 
$ sudo dnf install ffmpeg python3 python3-pip
```

### Arch
```
$ sudo pacman -S ffmpeg python python-pip
```

## Install the libraries

### Windows
Execute `windowsLibs.bat`

### Linux
```
$ chmod +x linuxLibs.sh
$ ./linuxLibs.sh
```

## How to get and use the bot
[Create a bot account and invite it](https://discordpy.readthedocs.io/en/stable/discord.html). Then edit variable `discord_token` with the token of your bot in `.env` file
```
git clone https://github.com/martinykrz/VinylBot.git
cd VinylBot/
python bot.py
```

## What it does
* Search and plays songs from Youtube and Spotify 
* Pause, resume and stop music
* Queue songs 
* Skip to the nth queued song
* Automatic removal of downloaded songs

## TODO
- [x] Fix low download rate because youtube-dl
- [x] No songs plays on Windows. *Maybe is the ffmpeg version*
- [] Make a better READ.md

## Thanks for make it possible
* The [examples](https://github.com/Rapptz/discord.py/tree/master/examples) and [documentation](https://discordpy.readthedocs.io/) of [discord.py](https://github.com/Rapptz/discord.py)
* This [StackOverflow question](https://stackoverflow.com/questions/60489888/how-to-use-a-key-words-instead-of-a-url-with-youtube-dl-and-discord-py)
* The basic/median information on this [link](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python)
* The inspiration to fix the automatic playing of queued songs on this [repo](https://github.com/Penguin1212/Discord-Bot-BotSpud)

