from get_deezer import get_track_link, get_album_link
from get_spotifyplaylist import get_spotify_playlist
import os
import pexpect

def downloadmusic():
    pass

current_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(current_dir, 'music')
deezer_url = 'https://www.deezer.com/en/track/1503443322'

child = pexpect.spawn('deemix -b flac -p ' + download_dir + ' ' + deezer_url)
child.expect('All done!')
print(child.before)
