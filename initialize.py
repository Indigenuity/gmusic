from gmusicapi import Mobileclient

# This only needs to be run once.  Re-use the creds from where it is stored
api = Mobileclient()
api.perform_oauth(storage_filepath="/Users/jd/ws/gmusic/.creds", open_browser=True)


