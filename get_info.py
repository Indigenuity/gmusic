from gmusicapi import Mobileclient
import os
import json

STORAGE_PATH = "/Users/jd/ws/gmusic"
CREDS_PATH = os.path.join(STORAGE_PATH, ".creds")
DEVICES_PATH = os.path.join(STORAGE_PATH, "registered_devices.json")
LIBRARY_PATH = os.path.join(STORAGE_PATH, "library.json")
PLAYLIST_INFO_PATH = os.path.join(STORAGE_PATH, "all_playlists.json")
PLAYLIST_CONTENT_PATH = os.path.join(STORAGE_PATH, "playlists")

DEVICE_ID = "342e914abacc484d"

print("Logging in")
api = Mobileclient()
api.oauth_login(device_id=DEVICE_ID, oauth_credentials=CREDS_PATH)
# => True

print("Getting registered devices")
with open(DEVICES_PATH, "w") as f:
    registered_devices = api.get_registered_devices()
    json.dump(registered_devices, f)

print("Getting all songs in library")
with open(LIBRARY_PATH, "w") as f:
    library = api.get_all_songs()
    json.dump(library, f)

print("Getting all playlists")
with open(PLAYLIST_INFO_PATH, "w") as f:
    playlists = api.get_all_playlists()
    json.dump(playlists, f)

print("Getting playlist contents")
if not os.path.exists(PLAYLIST_CONTENT_PATH):
    os.makedirs(PLAYLIST_CONTENT_PATH)

playlist_contents = api.get_all_user_playlist_contents()
for playlist in playlist_contents:
    playlist_name = "".join([x if x.isalnum() else "_" for x in playlist["name"]])
    playlist_filename = "{}.json".format(os.path.join(PLAYLIST_CONTENT_PATH, playlist_name))
    print("Saving playlist '{}' as {}".format(playlist_name, playlist_filename))
    with open(playlist_filename, "w") as f:
        json.dump(playlist, f)


# "".join([x if x.isalnum() else "_" for x in s])



library = api.get_all_songs()
sweet_track_ids = [track['id'] for track in library
                   if track['artist'] == 'The Cat Empire']

playlist_id = api.create_playlist('Rad muzak')
api.add_songs_to_playlist(playlist_id, sweet_track_ids)