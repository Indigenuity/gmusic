import logging
import os
import tempfile

from file_storage import FileStorage
from thegoogs import TheGoogs

logger = logging.getLogger("gmusic")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

STORAGE_PATH = "/Users/jd/ws/gmusic/data"

thegoogs = TheGoogs()

storage = FileStorage(STORAGE_PATH)
libdata = storage.read_libdata()

for index, song in enumerate(libdata.uploaded_songs):

    if not storage.song_exists(song):
        logger.info("Downloading song {}/{}: {}".format(index, len(libdata.uploaded_songs), song["title"]))
        data = thegoogs.get_uploaded_song(song["id"])
        storage.write_song(data, song)
    else:
        logger.info("Skipping downloaded song: {}".format(song["title"]))

for index, song in enumerate(libdata.all_songs):
    if not storage.song_exists(song):
        logger.info("Downloading unowned song {}/{}: {}".format(index, len(libdata.all_songs), song["title"]))
        data = thegoogs.get_streamed_song(song["id"])
        storage.write_song(data, song)
    else:
        logger.info("Skipping downloaded song: {}".format(song["title"]))

