import os

from datetime import datetime
from file_storage import FileStorage
from gmusicapi import Mobileclient
from libdata import Libdata

STORAGE_PATH = "/Users/jd/ws/gmusic/data"
CREDS_PATH = os.path.join(STORAGE_PATH, ".creds")
TRACK_CONTENT_PATH = os.path.join(STORAGE_PATH, "raw_tracks")

# Tablet
DEVICE_ID = "342e914abacc484d"

print("Logging in")
api = Mobileclient()
api.oauth_login(device_id=DEVICE_ID, oauth_credentials=CREDS_PATH)

print("Getting registered devices")
registered_devices = api.get_registered_devices()
print("Getting all songs in library")
library = api.get_all_songs()
print("Getting all playlists")
playlists = api.get_all_playlists()
print("Getting playlist contents")
playlist_contents = api.get_all_user_playlist_contents()

libdata = Libdata(
    registered_devices=registered_devices,
    all_songs=library,
    playlist_metadata=playlists,
    playlists=playlist_contents
)

# storage_basename = datetime.utcfromtimestamp(datetime.utcnow()).strftime('%Y-%m-%d_%H_%M_%S')
storage = FileStorage(STORAGE_PATH)
storage.write_libdata(libdata)


# if not os.path.exists(TRACK_CONTENT_PATH):
#     os.makedirs(TRACK_CONTENT_PATH)
# for track in library[:10]:
#     track_title = "".join([x if x.isalnum() else "_" for x in track["title"]])
#     filename = "{}.mp3".format(os.path.join(TRACK_CONTENT_PATH, track_title))
#     print("Downloading {} and saving to {}".format(track['title'], filename))
#     stream_url = api.get_stream_url(track['id'])
#     response = urllib.request.urlopen(stream_url)
#     data = response.read()
#     with open(filename, "wb") as f:
#         f.write(data)
#     if 'storeId' in track:
#         print("has store id : {}".format(track['title']))
#     else:
#         print("no store id : {}".format(track['title']))
