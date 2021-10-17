from get_functions import get_track_link, get_album_link, get_spotify_playlist, get_spotify_playlist_name
import config
import os
import platform
import pexpect
import wexpect
from tabulate import tabulate

def downloadmusic(download_dir, deezer_url, arl):

    if platform.system() == 'Windows':  #spawns child using wepect/pexpect
        child = wexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)
    else:
        child = pexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)

    i = child.expect(['Paste here your arl:', 'Download URL got'], timeout=10)
    if i == 0:
        print('Requesting ARL')
        child.sendline(arl)
        print('Entering ARL...')
    elif i == 1:
        pass

    child.expect('All done!', timeout=120)

    return True




#Start of script
print('Starting Music Downloader...')
playlist = input('Enter Spotify Playlist URL: ')
#Gets tracks from spotify playlist
tracks = get_spotify_playlist(playlist, config.spotify_token)


#Checks playlist
print('\n' + tabulate(tracks, headers=['Track', 'Album', 'Artists']))
verify = input('Is playlist correct? (y/n) ')
if verify.lower() != 'y':
    exit()


#Gets Deezer links
print('\nGetting Deezer links')
progress = 0
for track in tracks:
    progress += 1
    link = get_track_link(track[0], track[1], track[2])
    tracks[progress - 1].append(link)
    if link == None:
        print('Failed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])
    else:
        print('Gotten [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])


#Create directory
name = get_spotify_playlist_name(playlist, config.spotify_token)
download_dir = os.path.join(config.download_dir, name)
try:
    os.mkdir(download_dir)
except FileExistsError:
    print(download_dir + ' already exists')


#Downloads tracks with deemix
print('\nDownloading tracks')
progress = 0
success = 0
for track in tracks:
    progress += 1
    try:
        downloadmusic(download_dir, track[3], config.deezer_arl)
        print('Completed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])
        success += 1
    except:
        print('Failed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])

print('Download complete! [' + str(success) + '/' + str(len(tracks)) +']')
