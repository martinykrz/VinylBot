# VinylBot
Very basic music discord bot 

## Dependecies
1. Programs
    * python
    * pip
    * ffmpeg

2. Libraries
    * os
    * json
    * discord.py
    * "discord.py[voice]"
    * python-dotenv
    * youtube-dl
    * youtube-search

## How to install the dependecies

### Windows 
* To install the ffmpeg library in Windows, use the [link](https://windowsloop.com/install-ffmpeg-windows-10/) and follow the instructions
* To install python, use this [link](https://www.python.org/downloads/), download the .exe file and choose the recommended (if you don't know what you doing) or the custom one (select the option to install pip); don't forget to check the "Add to PATH Python3.x"
* If you installed python like the preview item, you may already have pip. To check if you have it, type in cmd `pip -V` and it will give you something like `pip 20.x.y ...`; else download this [file](https://bootstrap.pypa.io/get-pip.py) and type in cmd `python C:\path\to\get-pip.py`
* To install the libraries, type in cmd `pip install -U [library]` 

### Linux

#### Debian/Ubuntu
```
$ sudo apt update 
$ sudo apt install python3 ffmpeg python3-pip
$ pip install -U [library]
```

### Fedora
``` 
$ sudo dnf install ffmpeg python3 python3-pip
$ pip install -U [library]
```

### Arch
```
$ sudo pacman -S ffmpeg python python-pip
$ pip install -U [library]
```

## How to get and use the bot
1. Before use it, in the variables `files1` and `files2`, replace `\path\to\bot.py` with your path to the file bot.py. 
Afte edit that, type in the terminal or in cmd
```
git clone https://github.com/martinykrz/VinylBot.git
cd VinylBot/
```
2. Once you clone it, get the discord token following this [instructons](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python) adn edit in the the file `.env`, inside the variable `discord_token`
3. Finally, you can type in the terminal or in cmd
```
python bot.py
```

## What it does
* Search and plays a song from Youtube
* Pause, resume and stop music
* Makes a queue when a song is playing
* Skip to the nth queued song
* Automatic removal of downloaded songs

### Limitation of the bot
The only limitation that the bot has is that it's not an automatic reproduction of a queue of songs a.k.a you have to tell the bot to play the next song with a command

## References
* The [examples](https://github.com/Rapptz/discord.py/tree/master/examples) and [documentation](https://discordpy.readthedocs.io/) of [discord.py](https://github.com/Rapptz/discord.py)
* This [StackOverflow question](https://stackoverflow.com/questions/60489888/how-to-use-a-key-words-instead-of-a-url-with-youtube-dl-and-discord-py)
* The basic/median information on this [link](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python)

## TODO
- [] Remove the limitation
- [] Automate the replacement of the variables `files1` and `files2`
- [] Make a better READ.md
