# spotify-playlist-downloader
Download your Spotify playlists automatically as mp3-files. 
This script can read your playlists through a Spotify Developer Application and will search for corresponding media on YouTube, then download them via `youtube-dl`. Files will be downloaded in `webm` format and automatically converted into `mp3` files afterwards. Already downloaded files will be skipped when refreshing a downloaded playlist.


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs it didn't already download


### Requirements
Apart from the Python requirements that are described in the Installation chapter, `ffmpeg` needs to be installed on your system.
It can be downloaded [here](https://ffmpeg.org/download.html).

It's already included in the Windows releases.


### Installation
Works with [Python 3](https://www.python.org/downloads/).

* Needed packages: `unidecode`, `eyed3`, `youtube_dl`, `spotipy`
    * can be installed by running `pip install -r requirements.txt`

### Usage

* Usage: `python download.py` or `./download.py`
* For usage information: `python download.py -h`

```
$ python download.py -h
    usage: download.py [-h] [-r] [-f FOLDER] [-c] [--skip SKIP] [-csv CSV]

    optional arguments:
    -h, --help            show this help message and exit
    -r, --reset           remove all stored login data
    -f FOLDER, --folder FOLDER
                          keep the files in the folder specified
    -c, --create          try to create folder if doesn't exist
    --skip SKIP           number of songs to skip from the start of csv
    -csv CSV              input csv file
```

### Downloading playlist

You will be led through the configuration procedure when you first run the script.

1. Download through User Login
    * Login to your Spotify account and create a [Spotify Application](https://developer.spotify.com/my-applications/#!/applications)
    Through this the app can access your playlist. Make sure not to share the `spotify_variables.txt` file with anyone. When running the script, you will be led through this procedure.
        To do this, you need to do the following steps:
        1. Login to https://developer.spotify.com/dashboard/applications
        2. Click on 'Create an App' and enter a name and description for it. Both don't matter after they're set.
        3. Enable both checkboxes on the bottom of the prompt and click 'Create'.
        4. Click in 'Edit Settings'.
        5. Under 'Redirect URIs', add 'http://localhost/' and click 'Add', then 'Save'.
        6. Click on 'Show Client Secret'.
        7. Copy and paste the ID and the secret here.

        * You will be redirected to login into your Spotify account on your default web browser. After successful login you just need to copy the whole `http://localhost/?code=...` URL from your browser and paste it to the console where your script is running.
    * In case your Spotify account is linked with your facebook account, use your device username in the `username` argument for the script and use your device password to log in to spotify in the browser window that opens.

2. Download through CSV File
    * Convert your Spotify playlists to a CSV table from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))