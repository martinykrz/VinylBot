#!/usr/bin/env python
import os, json, yt_dlp, subprocess
from youtube_search import YoutubeSearch
from ytmusicapi import YTMusic
from spotdl.utils.spotify import SpotifyClient
from spotdl.types.song import Song

class Music:
    def __init__(self):
        self.song = ''
        self.name = ''
        self.author = ''
        self.path = "{}/Music/".format(os.path.expanduser("~"))
        self.exit = False
        #Spotify Client
        client_id = 'adfb10751507481fbd3d75b2b1c36d9e'
        client_secret = 'ac72e6687cd84568801bfe9c6709aa33'
        
        SpotifyClient.init(client_id, client_secret, False)
        
        self.ytmusic = YTMusic()
        
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            #bind to ipv4 since ipv6 addresses cause issues sometimes
        }
        
        # Quiet yt-dlp
        yt_dlp.utils.bug_reports_message = lambda:''
        
        self.ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
    
    def nameFilter(self):
        if 'spotify' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' spotify'))]
        elif 'local' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' local'))]
        elif 'playlist' in self.song:
            self.song = self.song[:len(list(self.song))-len(list(' playlist'))]
        else:
            pass

    def normalSong(self):
        if 'local' in self.song:
            self.nameFilter()
        else:
            yt = YoutubeSearch(self.song, max_results=1).to_json()
            self.song = 'https://www.youtube.com/watch?v=' + str(json.loads(yt)['videos'][0]['id'])
            self.name = self.ytdl.extract_info(self.song, download=False).get('title', None)
            self.author = str(json.loads(yt)['videos'][0]['channel'])

    def spotifySong(self):
        if 'track' in self.song:
            self.name = Song.from_url(self.song).name
            self.song = 'https://www.youtube.com/watch?v=' + ytmusic.search(self.name, 'songs')[0]['videoId']
            self.author = self.ytmusic.search(title, 'songs')[0]['artists'][0]['name']
        else:
            self.nameFilter()
            ytm = self.ytmusic.search(self.song, 'songs')[0]
            self.song = 'https://www.youtube.com/watch?v=' + ytm['videoId']
            self.name = ytm['title']
            self.author = ytm['artists'][0]['name']

    def urlSong(self):
        self.name = self.ytdl.extract_info(self.song, download=False).get('title', None)
        self.author = str(json.loads(YoutubeSearch(self.name, max_results=1).to_json())['videos'][0]['channel'])

    def makeTrack(self):
        if 'spotify' in self.song:
            self.spotifySong()
        elif 'youtube.com' in self.song or 'youtu.be' in self.song:
            self.urlSong()
        else:
            self.normalSong()

    def download(self, song):
        self.song = song
        print("\x1b[35;3mDownloading... \x1b[0;0m")
        subprocess.run([
            "yt-dlp",
            "-P",
            self.path,
            "-x",
            "--audio-format",
            "mp3",
            self.song
        ])

    def play(self, song):
        self.song = song
        self.makeTrack()
        print(f"\x1b[1;32;40mName: {self.name} \x1b[0;0m")
        print(f"\x1b[1;32;40mFrom: {self.author} \x1b[0;0m")
        subprocess.run([
            "mpv",
            "--no-video",
            "--volume=60",
            self.song
        ])

    def playlist(self, song):
        self.song = song
        if 'open.spotify.com/album/' in song:
            albumName = SpotifyClient().album(self.song)["name"]
            print(f"\x1b[35;49;1m{albumName}\x1b[0m")
            for track in SpotifyClient().album_tracks(self.song)["items"]:
                nameSong = track["name"]
                self.play(f"{nameSong} spotify")
        elif 'open.spotify.com/playlist' in song:
            playlistName = SpotifyClient().playlist(self.song)["name"]
            print(f"\x1b[35;49;1m{playlistName}\x1b[0m")
            for track in SpotifyClient().playlist_tracks(self.song)["items"]:
                nameSong = track["track"]["name"]
                self.play(f"{nameSong} spotify")
        else:
            self.nameFilter()
            with open(f"{self.path}{self.song}.txt", 'r') as pl:
                for s in pl:
                    tmp = list(s)
                    res = ''
                    i = 0
                    while tmp[i] != '\n':
                        res += tmp[i]
                        i += 1
                    self.play(res)
        print("\x1b[0;31;40mExit \x1b[0;0m")
        self.exit = True

    def songData(self, song):
        self.song = song
        self.makeTrack()
        return self.song, self.name, self.author

def main():
    m = Music()
    if not os.path.isdir(m.path):
        os.mkdir(m.path)
    while not m.exit:
        try:
            song = str(input("\x1b[1;33;40mSong/URL/Playlist/Download: \x1b[0;0m"))
            if 'download' in song:
                m.download(song)
            elif 'playlist' in song or 'album' in song:
                m.playlist(song)
            else:
                m.play(song)
        except KeyboardInterrupt:
            print('\r')
            print("\x1b[0;31;40mExit \x1b[0;0m")
            break

if __name__ == '__main__':
    main()
