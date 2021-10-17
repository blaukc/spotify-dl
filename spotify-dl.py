from get_functions import get_track_link, get_album_link, get_spotify_playlist, get_spotify_album, get_spotify_playlist_name, get_spotify_endpoint, download_track, download_album
import config
import os
from tabulate import tabulate
import argparse


def if_verbose(text, verbose):
    if verbose:
        print(text)


def spotify_dl_playlist(endpoint, verbose):
    #Get playlist name & album artist
    name, album_artist = get_spotify_playlist_name(endpoint, config.spotify_token, 'playlist')


    #Create directory
    download_dir = os.path.join(config.download_dir, name)
    try:
        os.mkdir(download_dir)
    except FileExistsError:
        print(download_dir + ' already exists')


    #Gets tracks from spotify playlist
    tracks = get_spotify_playlist(endpoint, config.spotify_token)


    #Checks playlist
    if verbose:
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
            if_verbose('Failed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0], verbose)
        else:
            if_verbose('Gotten [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0], verbose)
            if_verbose(link, verbose)



    #Downloads tracks with deemix
    print('\nDownloading tracks')
    progress = 0
    success = 0
    for track in tracks:
        progress += 1
        try:
            download_track(download_dir, track[3], config.deezer_arl)
            if_verbose('Completed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0], verbose)
            success += 1
        except Exception as e:
            if_verbose('Failed [' + str(progress) + '/' + str(len(tracks)) + ']: ' + track[0], verbose)
            print(e)

    print('\nDownload complete! [' + str(success) + '/' + str(len(tracks)) +']')





def spotify_dl_album(endpoint, verbose):
    #Get playlist name & album artist
    name, album_artist = get_spotify_playlist_name(endpoint, config.spotify_token, 'album')


    #Gets tracks from spotify playlist
    tracks = get_spotify_album(endpoint, config.spotify_token, name)


    #Checks playlist
    if verbose:
        print('\n' + tabulate(tracks, headers=['Track', 'Album', 'Artists']))
        verify = input('Is playlist correct? (y/n) ')
        if verify.lower() != 'y':
            exit()


    #Gets Deezer links
    print('\nGetting Deezer links')
    link = get_album_link(name, album_artist)
    if link == None:
        if_verbose('Unable to get album: ' + name, verbose)
    else:
        if_verbose('Gotten album link: ' + name, verbose)
        if_verbose(link, verbose)



    #Downloads tracks with deemix
    print('\nDownloading tracks')
    download_album(config.download_dir, link, config.deezer_arl, str(len(tracks)), if_verbose, verbose)



def spotify_dl(spotify_url, verbose=False):
    #Start of script
    print('Starting Music Downloader...')
    # playlist = input('Enter Spotify Playlist URL: ')

    #Gets spotify web api endpoint and checks if url is album/playlist
    endpoint, type = get_spotify_endpoint(spotify_url)

    if type == 'playlist':
        spotify_dl_playlist(endpoint, verbose)
    elif type == 'album':
        spotify_dl_album(endpoint, verbose)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='spotify playlist downloader')
    parser.add_argument('-v', '--verbose', action='store_true', help='turn on verbose mode')
    parser.add_argument('playlist_URL', help='Spotify Playlist URL')

    args = parser.parse_args()

    spotify_dl(args.playlist_URL, args.verbose)
