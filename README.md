# VinylBot
Very basic music discord bot 

## Install Dependecies
* [Windows Method](https://github.com/martinykrz/VinylBot/blob/main/WindowsInstall.md)
* [Linux Method](https://github.com/martinykrz/VinylBot/blob/main/LinuxInstall.md)

## Install libraries and get started
1. [Create a bot account and invite it](https://discordpy.readthedocs.io/en/stable/discord.html) 
2. Clone or unzip this repo
3. Type on the command line `dotenv set discord_token yourToken`
4. To start the bot type `python bot.py` or `python3 bot.py`

## What it does
* Search and plays songs from Youtube and Spotify 
* Pause, resume and stop music
* Queue songs 
* Skip to the nth queued song
* Automatic removal of downloaded songs

## TODO
- [x] Fix low download rate because youtube-dl
- [] Enable Spotify Playlist and Custom Playlist
- [] Replace discord.py with py-cord
- [] Make a better READ.md

## Thanks for make it possible
* The examples and documentation of [discord.py](https://github.com/Rapptz/discord.py)
* This [StackOverflow question](https://stackoverflow.com/questions/60489888/how-to-use-a-key-words-instead-of-a-url-with-youtube-dl-and-discord-py)
* The basic/median information on this [link](https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python)
* The inspiration to fix the automatic playing of queued songs on this [repo](https://github.com/Penguin1212/Discord-Bot-BotSpud)

