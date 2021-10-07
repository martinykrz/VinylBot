#!/bin/bash

echo "===Installing==="

libs='subprocess youtube-dl discord.py discord.py[voice] python-dotenv spotdl youtube-search platform'

for pkg in $libs
do 
    pip install $pkg
done

echo "===Installed==="

