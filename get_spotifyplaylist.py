import requests
import re

def remove_brackets(string):
    string = re.sub(r'\([^\(\)]*\)', '', string)    #remove all bracketed things

    while string[0] == ' ':                         #remove leftover spacings front
        string = string[1:]
    while string[-1] == ' ':                        #remove leftover spacings back
        string = string[:-1]

    return string



def get_spotify_endpoint(playlist_url):
    try:
        playlist_id = re.findall(r'playlist\/([^\?]*)', playlist_url)[0]        #formats playlist_url to get the playlist_id
    except:
        print('Invalid Spotify playlist URL')
        exit()

    url = 'https://api.spotify.com/v1/playlists/' + playlist_id
    return url



def get_spotify_playlist(playlist_url, token):
    url = get_spotify_endpoint(playlist_url) + '/tracks?fields=items.track(name%2Cartists.name%2Calbum.name)'    #adds fields to narrow spotify web api search
    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    try:
        r = requests.get(url, headers = headers)        #send get request
        parsed = r.json()['items']                      #parse json
    except:
        print('Playlist link wrong or token expired')
        exit()

    #formats the parsed json into a tracks list
    tracks = []
    for song_info in parsed:                             #output is in form {'track': {'album': {'name': 'allthefeels'}, 'artists': [{'name': 'emawk'}], 'name': 'bayridge'}}
        #getting tracks, album, artist from parsed data
        song_info = song_info['track']
        album = song_info['album']['name']
        artists = []
        for artist in song_info['artists']:
            artists.append(artist['name'])
        track = song_info['name']

        #remove brackets from track name and album name
        track = remove_brackets(track)
        album = remove_brackets(album)

        tracks.append([track, album, artists])

    return(tracks)

# token = 'BQCR2YfN7TL_i2UXzHvZL-qmHgsrjhwh-Lt6Htmy4fkzmPxXOWtqOSEXQ41TGHzX-n1477Owayc97a-YInfTo36E-MOB2G_yQaFCSaix6B2BE4cymaw5_tv-npWI0MzoMfcmHijuaq_kyekUJDvzmtH9eoHD'
# playlist_url = 'https://open.spotify.com/playlist/74ehSzUe6SOWerO6VhlgCP?si=504cecd132194c0c'
# get_spotify_playlist(playlist_url, token)



def get_spotify_playlist_name(playlist_url, token):
    url = get_spotify_endpoint(playlist_url) + '?fields=name'    #adds fields to narrow spotify web api search
    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    try:
        r = requests.get(url, headers = headers)        #send get request
        parsed = r.json()['items']                      #parse json
    except:
        print('Playlist link wrong or token expired')
        exit()
        
    return parsed
