::Install VS C++ Buils Tools
powershell "Invoke-WebRequest https://aka.ms/vs/17/release/VC_redist.x64.exe -Outfile .\tools.exe"
powershell "Start-Process .\tools.exe RunAs"
powershell "Remove-Item .\tools.exe"

::Other libraries
pip install yt-dlp
pip install numpy
pip install -U discord.py
pip install -U "discord.py[voice]"
pip install python-dotenv
pip install spotdl
pip install youtube-search
