# spotify-playlist-downloader
Download your Spotify playlists using simple python script


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs it didn't already download


### Installation
Works only with [Python 2.7](https://www.python.org/downloads/release/python-2717/). Currently working on a new version for Python 3.

### Downloading playlist

* Usage: `python2 download.py`
* For usage information: `python2 download.py -h`

1. Download through User Login
    * Login to your Spotify account and create a [Spotify Application](https://developer.spotify.com/my-applications/#!/applications)
    Through this the app can access your playlist. Make sure not to share the `spotify_variables.txt` file with anyone.
    
        Need to set new login data. for this, a Client-ID, Client-Secret and your Spotify username is needed.
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
    * Convert your Spotify playlists to a CSV tabke from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))