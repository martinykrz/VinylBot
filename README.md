# VinylBot
Very basic music discord bot 

## Dependecies
1. Programs
    * python
    * pip
    * ffmpeg
    * [Microsoft Visual Studio C++ Build Tools](https://aka.ms/vs/17/release/VC_redist.x64.exe) *Only for Windows*

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

## Install libraries and get started
1. [Create a bot account and invite it](https://discordpy.readthedocs.io/en/stable/discord.html). 
2. Clone this repo or download the zip file and uncompress it.
3. Execute the file
    - If you have Windows: open cmd or powershell, go to the file and execute `winInstallBot.bat` file
    - If you have Linux: open the terminal, go to the file and type `chmod +x linuxInstallBot.sh && ./linuxInstallBot.sh`
4. When `Discord Token: ` appears, copy the token created in the first step, paste it and press `Enter`
5. Once completed, you can use the bot by executing the `StartBot.bat` file on Windows or the `StartBot.sh` file on Linux in the similar way as the third step

## What it does
* Search and plays songs from Youtube and Spotify 
* Pause, resume and stop music
* Queue songs 
* Skip to the nth queued song
* Automatic removal of downloaded songs

## TODO
- [x] Fix low download rate because youtube-dl
- [] Make a better READ.md

## Thanks for make it possible
* The [examples](https://github.com/Rapptz/discord.py/tree/master/examples) and [documentation](https://discordpy.readthedocs.io/) of [discord.py](https://github.com/Rapptz/discord.py)
* This [StackOverflow question](https://stackoverflow.com/questions/60489888/how-to-use-a-key-words-instead-of-a-url-with-youtube-dl-and-discord-py)
* The basic/median information on this [link](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python)
* The inspiration to fix the automatic playing of queued songs on this [repo](https://github.com/Penguin1212/Discord-Bot-BotSpud)

