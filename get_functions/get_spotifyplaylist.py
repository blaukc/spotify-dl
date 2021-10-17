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
        if 'album' in playlist_url:
            playlist_id = re.findall(r'album\/([^\?]*)', playlist_url)[0]        #formats playlist_url to get the playlist_id
            type = 'album'
        else:
            playlist_id = re.findall(r'playlist\/([^\?]*)', playlist_url)[0]        #formats playlist_url to get the playlist_id
            type = 'playlist'
    except:
        print('Invalid Spotify playlist URL')
        exit()

    endpoint = 'https://api.spotify.com/v1/' + type + 's/' + playlist_id
    return endpoint, type



def get_spotify_playlist(endpoint, token):
    endpoint = endpoint + '/tracks?fields=items.track(name%2Cartists.name%2Calbum.name)'    #adds fields to narrow spotify web api search

    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    try:
        r = requests.get(endpoint, headers = headers)        #send get request
        parsed = r.json()['items']                      #parse json
    except Exception as e:
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


def get_spotify_album(endpoint, token, album):
    endpoint = endpoint + '/tracks'
    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    print(endpoint)
    try:
        r = requests.get(endpoint, headers = headers)        #send get request
        parsed = r.json()['items']                      #parse json
    except Exception as e:
        print(e)
        print('Playlist link wrong or token expired')
        exit()

    #formats the parsed json into a tracks list
    tracks = []
    for song_info in parsed:                             #output is very big, unable to use fields like in the playlist api
        artists = []
        for artist in song_info['artists']:
            artists.append(artist['name'])
        track = song_info['name']

        #remove brackets from track name and album name
        track = remove_brackets(track)
        album = remove_brackets(album)

        tracks.append([track, album, artists])

    return(tracks)


def get_spotify_playlist_name(endpoint, token, type):
    endpoint = endpoint + '?fields=name'   #adds fields to narrow spotify web api search
    headers = {'Accept': 'application/json','Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    try:
        r = requests.get(endpoint, headers = headers)        #send get request
        parsed = r.json()                      #parse json
    except:
        print('Playlist link wrong or token expired')
        exit()

    name = parsed['name']
    if type == 'album':
        artists = []
        for artist in parsed['artists']:
            artists.append(artist['name'])
    else:
        artists = None

    return name, artists
