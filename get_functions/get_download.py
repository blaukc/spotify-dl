import platform
import pexpect
import wexpect
import re

#get download for individual tracks
def download_track(download_dir, deezer_url, arl):
    try:
        if platform.system() == 'Windows':  #spawns child using wepect/pexpect depending on OS
            child = wexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)
        else:
            child = pexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)

        i = child.expect(['Paste here your arl:', 'Download URL got'], timeout=10)
        if i == 0:              #if child requests ARL, reply with ARL
            print('Requesting ARL')
            child.sendline(arl)
            print('Entering ARL...')
        elif i == 1:            #if child starts downloading, continue
            pass
    except Exception as e:
        print(e)
        exit()

    child.expect('All done!', timeout=120)

    return True



#get download for album
def download_album(download_dir, deezer_url, arl, total_tracks, if_verbose, verbose):
    try:
        if platform.system() == 'Windows':  #spawns child using wepect/pexpect depending on OS
            child = wexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)
        else:
            child = pexpect.spawn('deemix -b flac -p ' + '\"' + download_dir + '\" ' + deezer_url)

        i = child.expect(['Paste here your arl:', 'Download URL got'], timeout=10)
        if i == 0:              #if child requests ARL, reply with ARL
            print('Requesting ARL')
            child.sendline(arl)
            print('Entering ARL...')
        elif i == 1:            #if child starts downloading, continue
            pass

    except Exception as e:
        print(e)
        exit()

    progress = 0
    while True:
        try:
            progress += 1
            i = child.expect(['Completed download of', 'All done!'], timeout=120)
            if i == 0:                  #if completed song download, output success
                completed_track = re.findall(r' - (.*).mp3', child.readline())
                if_verbose('Completed [' + str(progress) + '/' + total_tracks + ']: ' + completed_track[0], verbose)
            elif i == 1:                #if completed all song downloads, break and end function & program
                break
        except Exception as e:          #if error in song download, output failure
            print(e)
            if_verbose('Failed [' + str(progress) + '/' + total_tracks + ']: ', verbose)
