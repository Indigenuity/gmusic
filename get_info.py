import os

from datetime import datetime
from file_storage import FileStorage
from gmusicapi import Mobileclient, Musicmanager
from libdata import Libdata

STORAGE_PATH = "/Users/jd/ws/gmusic/data"
CREDS_PATH = os.path.join(STORAGE_PATH, ".creds")
MANAGER_CREDS_PATH = "/Users/jd/ws/gmusic/.manager_creds"
TRACK_CONTENT_PATH = os.path.join(STORAGE_PATH, "raw_tracks")

# Tablet
DEVICE_ID = "342e914abacc484d"
MAC_ADDRESS = "A2:C2:E2:CC:C7:37"

print("Logging in")
mobile = Mobileclient()
mobile.oauth_login(device_id=DEVICE_ID, oauth_credentials=CREDS_PATH)
manager = Musicmanager()
manager.login(uploader_id=MAC_ADDRESS, oauth_credentials=MANAGER_CREDS_PATH)

print("Getting registered devices")
registered_devices = mobile.get_registered_devices()
print("Getting all songs in library")
library = mobile.get_all_songs()
print("Getting all playlists")
playlists = mobile.get_all_playlists()
print("Getting playlist contents")
playlist_contents = mobile.get_all_user_playlist_contents()
print("Getting uploaded tracks")
uploaded_tracks = manager.get_uploaded_songs()
purchased_tracks = manager.get_purchased_songs()

print("quota? {}".format(manager.get_quota()))

libdata = Libdata(
    registered_devices=registered_devices,
    all_songs=library,
    playlist_metadata=playlists,
    playlists=playlist_contents,
    uploaded_songs=uploaded_tracks,
    purchased_songs=purchased_tracks
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
