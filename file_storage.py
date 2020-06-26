import eyed3
import json
import logging
import os

from libdata import Libdata

logger = logging.getLogger("gmusic")


class FileStorage:

    DEFAULT_STORAGE_PATH = os.path.expanduser("~/gmusic")

    def __init__(self, storage_path=None, json_indent=4):
        self.storage_path = storage_path if storage_path else self.DEFAULT_STORAGE_PATH
        logger.debug("Initializing FileStorage at {}".format(self.storage_path))
        self.__init_filenames()
        self.json_indent = json_indent

    def __init_filenames(self):
        self.libdata_dir = os.path.join(self.storage_path, "libdata")
        self.registered_devices_filename = os.path.join(self.libdata_dir, "registered_devices.json")
        self.all_songs_filename = os.path.join(self.libdata_dir, "all_songs.json")
        self.playlist_metadata_filename = os.path.join(self.libdata_dir, "playlist_metadata.json")
        self.playlist_content_dir = os.path.join(self.libdata_dir, "playlists")
        self.track_dir = os.path.join(self.storage_path, "tracks")
        self.uploaded_songs_filename = os.path.join(self.libdata_dir, "uploaded_songs.json")
        self.purchased_songs_filename = os.path.join(self.libdata_dir, "purchased_songs.json")

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

    # TODO Make a less restrictive safename function
    @staticmethod
    def safe_basename(unsafe_name):
        logger.debug("Converting unsafe filename : {}".format(unsafe_name))
        return "".join([x if x.isalnum() else "_" for x in unsafe_name])

    def song_filename(self, song):
        return os.path.join(self.track_dir, song["id"])

    def read_libdata(self):
        logger.info("Loading libdata from file_storage at {}".format(self.storage_path))
        registered_devices = self.read_json(self.registered_devices_filename)
        all_songs = self.read_json(self.all_songs_filename)
        playlist_metadata = self.read_json(self.playlist_metadata_filename)
        playlists = [self.read_json(os.path.join(self.playlist_content_dir, x)) for x in os.listdir(self.playlist_content_dir)]
        uploaded_songs = self.read_json(self.uploaded_songs_filename)
        purchased_songs = self.read_json(self.purchased_songs_filename)
        # for filename in os.listdir(self.playlist_content_dir):
        return Libdata(
            registered_devices=registered_devices,
            all_songs=all_songs,
            playlist_metadata=playlist_metadata,
            playlists=playlists,
            uploaded_songs=uploaded_songs,
            purchased_songs=purchased_songs
        )

    def write_libdata(self, libdata):
        logger.info("Writing libdata to file_storage at {}".format(self.storage_path))
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        if not os.path.exists(self.playlist_content_dir):
            os.makedirs(self.playlist_content_dir)
        self.write_json(libdata.registered_devices, self.registered_devices_filename)
        self.write_json(libdata.all_songs, self.all_songs_filename)
        self.write_json(libdata.playlist_metadata, self.playlist_metadata_filename)
        for playlist in libdata.playlists:
            playlist_filename = os.path.join(self.playlist_content_dir, self.safe_basename(playlist["name"]))
            self.write_json(playlist, playlist_filename)
        self.write_json(libdata.uploaded_songs, self.uploaded_songs_filename)
        self.write_json(libdata.purchased_songs, self.purchased_songs_filename)

    def write_song(self, data, metadata):
        if not os.path.exists(self.track_dir):
            os.makedirs(self.track_dir)
        filename = self.song_filename(metadata)
        logger.info("Writing song '{}' to {}".format(metadata["title"], filename))
        with open(filename, "wb") as f:
            f.write(data)

        mp3 = eyed3.load(filename)
        if mp3.tag:
            # Remove the "owned by thegoogs" metadata
            mp3.tag.privates.remove(b'Google/OriginalClientId')
        else:
            mp3.initTag()
            mp3.tag.title = metadata["title"]
            mp3.tag.artist = metadata["artist"]
            mp3.tag.album = metadata["album"]
            mp3.tag.album_artist = metadata["albumArtist"]
            mp3.tag.track_num = metadata["trackNumber"]
            if metadata.get("composer"):
                mp3.tag.composer = metadata["composer"]
            if metadata.get("year"):
                mp3.tag.recording_date = metadata["year"]
        mp3.tag.save()

    def song_exists(self, song):
        filename = self.song_filename(song)
        return os.path.exists(filename)
