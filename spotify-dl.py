from get_functions import get_track_link, get_album_link, get_spotify_playlist, get_spotify_playlist_name
import os
import platform
import pexpect
import wexpect
from tabulate import tabulate

arl = '3dadffaa3ed08377420042cf0ede03f5f02fe54be0499fde032737b32b8c3632d08ddca191262e50a16ae8f001a6877141188a6692a8f2426d6af58036e74232e9502403c1c2db250326471544ffb97f8663fa79035e50b4425947e632d56ae0'
token = 'BQD4-8K1iv4qBgWykm45vO5sa3miB4HyZXckhvZfyf-z-dT_Ymj6FsdUMa0BBbsdKrM9JSKR5lWey0J4uugBIIXkLqHH-nODr4-zTFfy5pU7SeNQ-S_kckRz-HDMi-_iTDpFUuoAN0Hz_7GissCZ13c3rLFt'
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.join(current_dir, 'music')

def downloadmusic(download_dir, deezer_url, arl):

    if platform.system() == 'Windows':  #spawns child using wepect/pexpect
        child = wexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)
    else:
        child = pexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)

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
tracks = get_spotify_playlist(playlist, token)


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
name = get_spotify_playlist_name(playlist, token)
download_dir = os.path.join(target_dir, name)
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
        downloadmusic(download_dir, track[3], arl)
        print('Completed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])
        success += 1
    except:
        print('Failed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0])

print('Download complete! [' + str(success) + '/' + str(len(tracks)) +']')
