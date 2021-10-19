# Spotify-DL

Downloads Spotify playlists using [Spotify Web Api](https://developer.spotify.com/documentation/web-api/), [deemix](https://git.freezer.life/RemixDev/deemix-py) and [deezer-python](https://pypi.org/project/deezer-python/)

# Set up

Clone project

    git clone https://github.com/blaukc/spotify_dl.git

When in project directory, install requirements

See troubleshooting if you get errors

    pip install -r requirements.txt

## config.py

Open up config.py to change settings

### deezer_arl

Go to [Deezer](https://www.deezer.com/en/), create an account and get your arl by clicking on the https lock in your browser

![deezer arl 1](https://i.imgur.com/wuklDtW.png)

![deezer arl 2](https://i.imgur.com/2CjkZM6.png)

### spotify_token

Go to [Spotify Web Api](https://developer.spotify.com/console/get-album/) and request a token

![spotify token 1](https://i.imgur.com/IOU9fkv.png)

### download_dir

Enter the path where you want the music to be downloaded into

### bitrate

Choose one of the 3 options, if deemix unable to find bitrate, it will default to a lower bitrate

    bitrate = 'flac'
    bitrate = '320'
    bitrate - '128'

### timeout

Sets max download time for each song, before moving on to the next song

    timeout = 180

# Usage

When in project directory

    python spotify_dl.py [spotify playlist/album link]

Verbose mode

    python spotify_dl.py -v https://open.spotify.com/album/6pEz5WCvDGB8ved9AcouQ5


# Troubleshooting

### No Microsoft Visual C++

![error 1](https://i.imgur.com/8jcYL3i.png)

If experiencing this error, you need to download [Microsoft Visual C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Make sure to tick Desktop Development with C++ when installing

![error 2](https://i.imgur.com/VYenln4.png)
