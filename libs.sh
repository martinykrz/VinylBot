#!/bin/bash

echo "===Installing==="

libs='os sys json glob subprocess youtube-dl discord.py discord.py[voice] python-dotenv spotdl tinytag youtube-search platform'

for pkg in $libs
do 
    pip install $pkg
done

echo "===Installed==="

