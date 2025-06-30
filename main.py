import subprocess
import random
import yt_dlp
from tkinter import *

#I don't remember what requests and re used to do, but I'm leaving them in case I ever need them again
# import requests
# import re

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

    #I know now that a bunch of globals is bad practice, but I made this when I was
    #less experienced with Python. I'd just use a dictionary now.
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

    #Logic to prevent playing the same song twice in a row
    while True:
        currentsong = random.choice(chosenlist)
        if currentsong != lastsong:
            lastsong = currentsong
            break

    #Plays the song
    subprocess.run([mpv_path, '--no-video', currentsong])
    print("new song started")

#Automatically enters my own preferences and mpv file path
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

#Lets user set own playlist urls, weighting percentage, and mpv filepath
def normalsetup():

    global mainplaylistpercent
    global playlist1
    global playlist2
    global mpv_path

    mainplaylistpercent = int(ntrmainplaylistpercent.get())
    playlist1 = ntrplaylist1.get()
    playlist2 = ntrplaylist2.get()
    mpv_path = ntrmpvpath.get()

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

    window.destroy()

    while True:
        selectsong()

#dummy values for later logic
lastsong = "a"
currentsong = "a"
chosenlist = "a"

#Setting up the UI

window = Tk()
window.title("Weighted Playlist")
window.geometry('900x450')
window.tk.call('tk', 'scaling', 3)

lblinstructions = Label(window, text="To use default presets, click ""Fast Setup.""\nOtherwise, enter information below.").grid(column=0,row=0)
btnfastsetup = Button(window, text="Fast Setup", command=fastsetup).grid(column=1,row=0)

empty = Label(window).grid(column=0,row=1)

lblplaylist1 = Label(window, text="Input main playlist:").grid(column=0,row=2)
ntrplaylist1 = Entry(window)
ntrplaylist1.grid(column=1,row=2)

lblplaylist2 = Label(window, text="Input secondary playlist:").grid(column=0,row=3)
ntrplaylist2 = Entry(window)
ntrplaylist2.grid(column=1,row=3)

lblmpvpath = Label(window, text="Input mpv filepath:").grid(column=0,row=4)
ntrmpvpath = Entry(window)
ntrmpvpath.grid(column=1,row=4)

ntrmainplaylistpercent = Entry(window)
ntrmainplaylistpercent.grid(column=1,row=5)
lblmainplaylistpercent = Label(window, text="Input percentage you'd like the main playlist\nto play (an integer between 0 and 100):").grid(column=0,row=5)

btnbeginplaying = Button(window, text="Begin Playing", command=normalsetup).grid(column=1,row=6)

#Keeps window open for user input. It will close itself after mpv launches.
window.mainloop()