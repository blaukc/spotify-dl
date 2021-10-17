import platform
import pexpect
import wexpect
import re

def download_track(download_dir, deezer_url, arl):
    try:
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
    except Exception as e:
        print(e)
        exit()

    child.expect('All done!', timeout=120)

    return True

def download_album(download_dir, deezer_url, arl, total_tracks, if_verbose, verbose):
    try:
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

    except Exception as e:
        print(e)
        exit()

    progress = 0
    while True:
        try:
            progress += 1
            i = child.expect(['Completed download of', 'All done!'], timeout=120)
            if i == 0:
                completed_track = re.findall(r' - (.*).mp3', child.readline())
                if_verbose('Completed [' + str(progress) + '/' + total_tracks + ']: ' + completed_track[0], verbose)
            elif i == 1:
                break
        except Exception as e:
            print(e)
            if_verbose('Failed [' + str(progress) + '/' + total_tracks + ']: ', verbose)
