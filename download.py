#!/usr/bin/env python

import os
import re
import csv
import json
import eyed3
import argparse
import youtube_dl
import spotipy
import spotipy.util as util
from unidecode import unidecode


def get_songs_from_csvfile(csvfile, args):
    songs = []
    with open(csvfile, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the first line
        if args.skip:
            print('Skipping', args.skip, 'songs')
            for i in range(args.skip):
                next(reader)
        for row in reader:
            songs.append({
                'name': unidecode(row[0]).strip(),
                'artist': unidecode(row[1]).strip(),
                'album': unidecode(row[2]).strip()
            })
    return songs


def get_environment_variables():
    if not os.path.isfile('.login.json'):
        return {}
    with open('.login.json') as jsonfile:
        variables = json.load(jsonfile)
    return variables


def save_environment_variables(variables):
    variables['SPOTIPY_REDIRECT_URI'] = 'http://localhost/'
    with open('.login.json', 'w+') as jsonfile:
        json.dump(variables, jsonfile)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def download_finish(d):
    if d['status'] == 'finished':
        print('\x1b[1A\x1b[2K')
        print("\x1b[1A[\033[93mConverting\033[00m] %s" % d['filename'])


def download_songs(songs, folder):
    for song in songs:
        probable_filename = folder + '/' + song['name'] + ' - ' + \
            song['artist'] + '.mp3'
        if os.path.isfile(probable_filename):
            # The file may already be there, so skip
            print('[\033[93mSkipping\033[00m] %s by %s' % \
                (song['name'], song['artist']))
            continue
        opts = {
            'format': 'bestaudio/best',
            'forcejson': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
     #       'verbose': True,
            'progress_hooks': [download_finish],
            'logger': MyLogger(),
            'outtmpl': folder + '/' + song['name'] + ' - ' + song['artist'] + '.%(ext)s'
        }
        url = ' '.join([song['name'], song['artist'], 'audio', 'youtube'])
        url = 'ytsearch:' + url
        print('[\033[91mFetching\033[00m] %s' % probable_filename)
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([url])
        if os.path.isfile(probable_filename):
            afile = eyed3.load(probable_filename)
            afile.tag.title = song['name']
            afile.tag.artist = song['artist']
            afile.tag.album = song['album']
            afile.tag.save()
        else:
            print('\x1b[1A\x1b[2K')
            print('\x1b[1A[\033[91mMetadata\033[00m] Could not set metadata for %s\nTemp' % \
                probable_filename)

        print('\x1b[1A\x1b[2K')
        print('\x1b[1A[\033[92mDownloaded]\033[00m', song['name'], '-', song['artist'])


def get_songs_from_playlist(tracks, args):
    songs = []
    for item in tracks['items'][args.skip:]:
        track = item['track']
        songs.append({
            'name': unidecode(track['name']).strip(),
            'artist': unidecode(track['artists'][0]['name']).strip(),
            'album': unidecode(track['album']['name']).strip()
        })
    return songs


#https://stackoverflow.com/a/1548720/7195897
def purge(dir, pattern):
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reset', help="remove all stored login data", action='store_true')
    parser.add_argument('-f', '--folder', help="keep the files in the folder specified")
    parser.add_argument('-c', '--create', help="try to create folder if doesn't exist",
                        action="store_true")
    parser.add_argument('--skip', help="number of songs to skip from the start of csv",
                        type=int)
    parser.add_argument('-csv', help="input csv file")

    args = parser.parse_args()

    # getting current working directory
    folder = os.path.dirname(os.path.realpath(__file__))

    if args.folder:
        if os.path.isdir(args.folder):
            folder = os.path.abspath(args.folder)
        elif args.create:
            try:
                os.makedirs(args.folder)
                folder = os.path.abspath(args.folder)
            except e:
                print('Error while creating folder')
                raise
        else:
            print('No such folder. Aborting..')
            exit()
        print('Storing files in', folder)

    if args.csv:
        if os.path.isfile(args.csv):
            csvfile = args.csv
            songs = get_songs_from_csvfile(csvfile, args)
            download_songs(songs, folder)
        else:
            print('No such csv file. Aborting..')
            exit()

    if args.reset:
        path = os.path.dirname(os.path.abspath(__file__))

        purge(path, '\.cache-.*')
        purge(path, '.login.json')
        
        print("'-r': successfully removed stored login data.")

    else:
        parser.print_help()

    variables = get_environment_variables()
    if variables == {}:
        print("log: could not read valid variables from .login.json\n")
        print("Need to set new login data. for this, a Client-ID, Client-Secret and your Spotify username is needed.")
        print("To do this, you need to do the following steps:\n")
        print("\t1. Login to https://developer.spotify.com/dashboard/applications")
        print("\t2. Click on 'Create an App' and enter a name and description for it. Both don't matter after they're set.")
        print("\t3. Enable both checkboxes on the bottom of the prompt and click 'Create'.")
        print("\t4. Click in 'Edit Settings'.")
        print("\t5. Under 'Redirect URIs', add 'http://localhost/' and click 'Add', then 'Save'.")
        print("\t6. Click on 'Show Client Secret'.")
        print("\t7. Copy and paste the ID and the secret here.\n")
        variables['SPOTIPY_CLIENT_ID'] = input("Client-ID: ")
        variables['SPOTIPY_CLIENT_SECRET'] = input("Client-Secret: ")
        variables['USERNAME'] = input("Your Spotify-Username: ")
        save_environment_variables(variables)

        print("\nlog: user settings saved successfully\n")

        print("You will be redirected to login into your Spotify account on your web browser. After successful login you just need to copy the whole `http://localhost/?code=...` URL from your browser and paste it to this console.")

    scope = 'playlist-read playlist-read-private'
    token = util.prompt_for_user_token(variables['USERNAME'], scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        try:
            playlists = sp.user_playlists(variables['USERNAME'])
        except spotipy.client.SpotifyException:
            print("Invalid Username")
            exit()
        if len(playlists) > 0:
            print("\nAll your Playlists: ")
            for index, playlist in enumerate(playlists['items']):
                print(str(index + 1) + ": " + playlist['name'])
            n = input("Enter numbers of playlists you want to download (e.g. '4' or '4,7,8'): ").split(",")
            if n:
                for i in range(0, len(n), 2):
                    playlist_folder = folder+"/"+playlists['items'][int(n[i]) - 1]['name']
                    print('Storing files in', playlist_folder)
                    if not os.path.isdir(playlist_folder):
                        try:
                            os.makedirs(playlist_folder )
                        except e:
                            print('Error while creating folder')
                            raise
                    playlist_id = playlists['items'][int(n[i]) - 1]['id']
                    tracks = sp.user_playlist(variables['USERNAME'], playlist_id,
                                                fields="tracks,next")['tracks']
                    songs = get_songs_from_playlist(tracks, args)
                    download_songs(songs, playlist_folder )
            else:
                print("No numbers provided! Aborting...")
        else:
            print("No playlist found!")
    else:
        print("Can't get token for", variables['USERNAME'])
        exit()


if __name__ == '__main__':
    main()
