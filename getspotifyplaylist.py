import requests
import re

token = 'BQDSVzaD7ca0m-bSXHelMlnRII539g7Mh68sh4jFYgvQpnG5fe_01X2jeHuEUCGHQ5Q5muTKJsQAzIZJgU4xGisWxCdMwToVJtNwkR3448mo1wrnUlFYQcA0WXczM_vxX5Yy0qZHseKfkifmyO3ZgO4Nwru1'
playlist_url = 'https://open.spotify.com/playlist/74ehSzUe6SOWerO6VhlgCP?si=504cecd132194c0c'

def get_spotify_playlist(playlist_url, token):
    playlist_id = re.findall(r'playlist\/([^\?]*)', playlist_url)[0]
    url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?fields=items.track(name%2Cartists.name%2Calbum.name)'
    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    r = requests.get(url, headers = headers)        #send get request
    parsed = r.json()['items']                      #parse json

    tracks = []
    for song in parsed:                             #output is in form {'track': {'album': {'name': 'allthefeels'}, 'artists': [{'name': 'emawk'}], 'name': 'bayridge'}}
        song = song['track']
        album = song['album']['name']
        artists = []
        for artist in song['artists']:
            artists.append(artist['name'])
        track = song['name']

        tracks.append([track, album, artists])

    print(tracks)

get_spotify_playlist(playlist_url, token)
