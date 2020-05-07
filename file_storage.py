import json
from libdata import Libdata
import logging
import os

logger = logging.getLogger(__name__)


class FileStorage:

    DEFAULT_STORAGE_PATH = os.path.expanduser("~/gmusic")

    def __init__(self, storage_path=None, json_indent=4):
        self.storage_path = storage_path if storage_path else self.DEFAULT_STORAGE_PATH
        logger.debug("Initializing FileStorage at {}".format(self.storage_path))
        self.__init_filenames()
        self.json_indent = json_indent

    @staticmethod
    def write_json(data, filename):
        logger.debug("Writing {}".format(filename))
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def read_json(filename):
        logger.debug("Reading {}".format(filename))
        with open(filename, "r") as f:
            return json.load(f)

    def read_libdata(self):
        logger.info("Loading libdata from file_storage at {}".format(self.storage_path))
        registered_devices = self.read_json(self.registered_devices_filename)
        all_songs = self.read_json(self.all_songs_filename)
        playlist_metadata = self.read_json(self.playlist_metadata_filename)
        playlists = [self.read_json(x) for x in os.listdir(self.playlist_content_dir)]
        # for filename in os.listdir(self.playlist_content_dir):
        return Libdata(
            registered_devices=registered_devices,
            all_songs=all_songs,
            playlist_metadata=playlist_metadata,
            playlists=playlists
        )

    def write_libdata(self, libdata):
        logger.info("Writing libdata to file_storage at {}".format(self.storage_path))
        self.write_json(libdata.registered_devices, self.registered_devices_filename)
        self.write_json(libdata.all_songs, self.all_songs_filename)
        self.write_json(libdata.playlist_metadata, self.playlist_metadata_filename)
        for playlist in libdata.playlists:
            playlist_basename = "".join([x if x.isalnum() else "_" for x in playlist["name"]])
            playlist_filename = os.path.join(self.playlist_content_dir, playlist_basename)
            self.write_json(playlist, playlist_filename)

    def __init_filenames(self):
        self.libdata_dir = os.path.join(self.storage_path, "libdata")
        self.registered_devices_filename = os.path.join(self.libdata_dir, "registered_devices.json")
        self.all_songs_filename = os.path.join(self.libdata_dir, "all_songs.json")
        self.playlist_metadata_filename = os.path.join(self.libdata_dir, "playlist_metadata.json")
        self.playlist_content_dir = os.path.join(self.libdata_dir, "playlists")