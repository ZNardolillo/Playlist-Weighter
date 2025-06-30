# Playlist-Weighter
This tool allows a user to select two separate youtube playlists and play songs from each. Songs are played locally using mpv, which happens to bypass ads as an added benefit.

The user sets how much each list is weighted - The intended functionality of this is to pull songs from a very large list of old liked songs, and also draw from a current playlist of new liked songs at a much higher rate.

This requires mpv to be installed. "Fast Setup" currently defaults to my exact needs. If I improve this tool in the future, I'll add functionality to save user preferences and set them to fast setup.

Other avenues of improvement:

Add the ability to draw from any number of playlists, not just 2
Add a log for the title of each song played instead of just "new song started"
Some songs wind up sounding abnormally quiet, but all my attempts at normalizing the volume result in every individual song having the same volume throughout, which just sounded wrong for songs with big peaks and valleys
Make the Tkinter UI less hideous
Try to autodetect mpv filepath
Remove use of global variables
Add functionality for media players other than mpv
