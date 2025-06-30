import subprocess
# import requests
# import re
import random
import yt_dlp
# from tkinter import *

#Uses yt_dlp to get every individual song url from a given playlist url
def getplaylisturls(playlist):
    ydl_opts = {
        'quiet': True,
        'ignoreerrors': True,
        'extract_flat': 'in_playlist'
    }

    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist, download=False)

        #Only adds publicly listed videos to the list, otherwise mpv won't be able to play private videos

        if playlist_info and 'entries' in playlist_info:
            for entry in playlist_info['entries']:
                if (
                        entry and
                        entry.get('id') and
                        entry.get('title') and
                        'Private video' not in entry['title'] and
                        'Deleted video' not in entry['title']
                ):
                    videos.append(f"https://www.youtube.com/watch?v={entry['id']}")

    return videos


#Randomly selects which playlist to pull from, then a random song from that playlist
def selectsong():

    global mainplaylistpercent
    global newsongs
    global oldsongs
    global mpv_path
    global currentsong
    global lastsong

    #Picks a random value between 1 and 100, weighs it against the user-defined
    #chance to pick from the main playlist, then picks a random song from either
    #the newsongs list or the oldsongs list

    randomfactor = random.randint(1,100)


    if randomfactor <= mainplaylistpercent:
        chosenlist = newsongs
    else:
        chosenlist = oldsongs

    while True:
        currentsong = random.choice(chosenlist)
        if currentsong != lastsong:
            lastsong = currentsong
            break

    #Plays the song
    subprocess.run([mpv_path, '--no-video', currentsong])
    print("new song started")

#Automatically enters my own preferences and mpv file path.
def fastsetup():

    global mainplaylistpercent
    global playlist1
    global playlist2
    global mpv_path

    mainplaylistpercent = 50
    playlist1 = "https://www.youtube.com/playlist?list=PLJlEi5wBnZ5Ye0tsv3hzt0y_d8ljmb0D8"
    playlist2 = "https://www.youtube.com/playlist?list=PLJlEi5wBnZ5aGaDrWNJs7pVwEZF4zQce4"
    mpv_path = r"C:\Users\Admin\Music\mpv\mpv.exe"

    start()



#Called from either setup function's end to allocate urls into two arrays, then loops the selectsong function
def start():

    global newsongs
    global oldsongs
    global playlist1
    global playlist2
    global currentsong

    newsongs = getplaylisturls(playlist1)
    oldsongs = getplaylisturls(playlist2)


    while True:
        selectsong()

#dummy values for later logic
lastsong = "a"
currentsong = "a"
chosenlist = "a"

fastsetup()