#!/bin/bash

echo "===Installing==="

libs='yt-dlp discord.py discord.py[voice] python-dotenv spotdl youtube-search'

for pkg in $libs
do 
    pip install $pkg
done

echo "===Installed==="

