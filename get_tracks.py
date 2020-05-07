import os

from file_storage import FileStorage
from gmusicapi import Musicmanager
from file_storage import FileStorage

STORAGE_PATH = "/Users/jd/ws/gmusic/data"
CREDS_PATH = "/Users/jd/ws/gmusic/.manager_creds"
MAC_ADDRESS = "A2:C2:E2:CC:C7:37"

api = Musicmanager()
api.login(uploader_id=MAC_ADDRESS, oauth_credentials=CREDS_PATH)

storage = FileStorage(STORAGE_PATH)
libdata = storage.read_libdata()

