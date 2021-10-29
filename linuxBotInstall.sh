#!/bin/bash

echo "=== Installing libraries ==="
libs='yt-dlp discord.py discord.py[voice] python-dotenv spotdl youtube-search'
for pkg in $libs
do 
    pip install $pkg
done
echo "=== Done ==="

echo "=== Creating VinylBot's own folder ==="
mkdir ~/bot 
cp bot.py ~/bot/.
echo "=== Done ==="

echo "=== Creating ENV file ==="
cd ~/bot 
echo "Discord Token: "
read token
dotenv set discord_token $token
dotenv set client_id adfb10751507481fbd3d75b2b1c36d9e
dotenv set client_secret ac72e6687cd84568801bfe9c6709aa33 
echo "=== Done ==="

echo "=== Creating StartBot.sh ==="
echo "python ~/bot/bot.py" > ~/bot/StartBot.sh
chmod +x ~/bot/StartBot.sh
echo "=== Done ==="
