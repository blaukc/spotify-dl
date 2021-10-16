from get_deezer import get_track_link, get_album_link
from get_spotifyplaylist import get_spotify_playlist
import os
import platform
import pexpect
import wexpect
from tabulate import tabulate

def downloadmusic(deezer_url, child):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_dir, 'music')
    #arl = '3dadffaa3ed08377420042cf0ede03f5f02fe54be0499fde032737b32b8c3632d08ddca191262e50a16ae8f001a6877141188a6692a8f2426d6af58036e74232e9502403c1c2db250326471544ffb97f8663fa79035e50b4425947e632d56ae0'

    i = child.expect(['Paste here your arl:', 'Downloading track'], timeout=5)
    if i == 0:
        arl = input('Enter your Deezer ARL: ')
        child.sendline(arl)
        print('Entering ARL...')
    elif i == 1:
        pass
    child.expect('All done!')
    print('Completed: ')


print('Starting Music Downloader...')
playlist = input('Enter Spotify Playlist URL: ')
token = input('Enter Spotify token: ')
#Gets tracks from spotify playlist
tracks = get_spotify_playlist(playlist, token)

#Checks playlist
print('\n' + tabulate(tracks, headers=['Track', 'Album', 'Artists']))
verify = input('Is playlist correct? (y/n) ')
if verify.lower() != 'y':
    exit()

#Gets Deezer links
print('\nGetting Deezer links')
links = []
progress = 0
for track in tracks:
    progress += 1
    link = get_track_link(track[0], track[1], track[2][0])
    links.append(link)
    if link == None:
        print('Unable to get ' + track[0] + ' ' + str(progress) + '/' + str(len(tracks)))
    else:
        print('Gotten ' + str(progress) + '/' + str(len(tracks)))

#Downloads tracks with deemix
print('\nDownloading tracks')
if platform.system() == 'Windows':  #spawns child using wepect/pexpect
    child = wexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)
else:
    child = pexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)
