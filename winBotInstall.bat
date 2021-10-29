@echo off

echo === Installing libraries ===
pip install yt-dlp
pip install numpy
pip install -U discord.py
pip install -U "discord.py[voice]"
pip install python-dotenv
pip install "python-dotenv[cli]"
pip install spotdl
pip install youtube-search
echo === Done ===

echo === Creating VinylBot's own folder ===
md C:\Users\%USERNAME%\Desktop\bot\
copy bot.py C:\Users\%USERNAME%\Desktop\bot\.
echo === Done ===

echo === Creating ENV file ===
cd C:\Users\%USERNAME%\Desktop\bot\
set /p token="Discord Token: "
dotenv set discord_token %token%
dotenv set client_id adfb10751507481fbd3d75b2b1c36d9e
dotenv set client_secret ac72e6687cd84568801bfe9c6709aa33 
echo === Done ===

echo === Creating StartBot.bat ===
echo python C:\Users\%USERNAME%\Desktop\bot\bot.py > C:\Users\%USERNAME%\Desktop\StartBot.bat 
echo === Done ===
