#!/bin/bash

echo "===Installing==="

libs='subprocess yt-dlp discord.py discord.py[voice] python-dotenv spotdl youtube-search platform'

for pkg in $libs
do 
    pip install $pkg
done

echo "===Installed==="

