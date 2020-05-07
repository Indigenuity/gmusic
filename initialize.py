from gmusicapi import Mobileclient, Musicmanager

# This only needs to be run once.  Re-use the creds from where it is stored
mobile = Mobileclient()
mobile.perform_oauth(storage_filepath="/Users/jd/ws/gmusic/.creds", open_browser=True)

manager = Musicmanager()
manager.perform_oauth(storage_filepath="/Users/jd/ws/gmusic/.manager_creds",open_browser=True)


