from get_deezer import get_track_link, get_album_link
from get_spotifyplaylist import get_spotify_playlist
import os
import platform
import pexpect
import wexpect

def downloadmusic():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_dir, 'music')
    deezer_url = 'https://www.deezer.com/en/track/1503443322'
    arl = '3dadffaa3ed08377420042cf0ede03f5f02fe54be0499fde032737b32b8c3632d08ddca191262e50a16ae8f001a6877141188a6692a8f2426d6af58036e74232e9502403c1c2db250326471544ffb97f8663fa79035e50b4425947e632d56ae0'


    if platform.system() == 'Windows':
        child = wexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)
    else:
        child = pexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)

    i = child.expect(['Paste here your arl:', 'Downloading track'], timeout=5)
    if i == 0:
        print('Requesting ARL...')
        child.sendline(arl)
        print('Pasting ARL...')
    elif i == 1:
        pass
    child.expect('All done!')
    print('Song has been downloaded!')


print('Starting Music Downloader...')
