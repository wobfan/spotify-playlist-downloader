# spotify-playlist-downloader
Download your Spotify playlists using simple python script


### Features
* Adds metadata to the downloaded songs (title, artist and album)
* Download only the songs it didn't already download


### Installation
Works only with [Python 2.7](https://www.python.org/downloads/release/python-2717/). Currently working on a new version for Python 3.

### Downloading playlist

* For usage information: `download.py -h`



1. Download through User Login
    * Login to your Spotify account and create a [Spotify Application](https://developer.spotify.com/my-applications/#!/applications)
    Through this the app can access your playlist. Make sure not to share the `spotify_variables.txt` file with anyone.
    
        * Set Redirect URIs = `http://localhost/` in your application settings and save it.
        * Set the Spotify variables in `spotify_variables.txt` like:

              SPOTIPY_CLIENT_ID='your-spotify-client-id'
              SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
              SPOTIPY_REDIRECT_URI='http://localhost/'

        * You will be redirected to login into you Spotify account on web browser. After successful login you just need to copy the whole `http://localhost/?code=...` URL from your browser and paste it to the console where your script is running.
    * In case your Spotify account is linked with your facebook account, use your device username in the `username` argument for the script and use your device password to log in to spotify in the browser window that opens.

2. Download through CSV File
    * Convert your spotify playlists to csv from [here](http://joellehman.com/playlist/) (Thanks to [Joel Lehman](https://github.com/jal278))