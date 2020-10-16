import datetime
import logging
import os
import urllib

from gmusicapi import Mobileclient, Musicmanager
from libdata import Libdata

logger = logging.getLogger("gmusic")


class TheGoogs:

    DEFAULT_CREDS_DIR = "~/gmusic/.oauth"
    DEFAULT_MOBILE_DEVICE_ID = "342e914abacc484d"       # Galaxy Tab
    DEFAULT_MANAGER_MAC_ADDRESS = "A2:C2:E2:CC:C7:37"   # Made-up

    def __init__(self, creds_dir=DEFAULT_CREDS_DIR):
        self.creds_dir = os.path.expanduser(creds_dir)
        logger.info("Creating TheGoogs from creds at {}".format(self.creds_dir))
        self.mobile_creds = os.path.join(self.creds_dir, "mobile.creds")
        self.manager_creds = os.path.join(self.creds_dir, "manager.creds")

        self.mobile = Mobileclient()
        self.manager = Musicmanager()

        logger.debug("Logging in")
        self.mobile.oauth_login(device_id=self.DEFAULT_MOBILE_DEVICE_ID, oauth_credentials=self.mobile_creds)
        self.manager.login(uploader_id=self.DEFAULT_MANAGER_MAC_ADDRESS, oauth_credentials=self.manager_creds)

    def get_libdata(self):
        logger.info("Fetching libdata ...")

        logger.info("... fetching registered devices")
        registered_devices = self.mobile.get_registered_devices()

        logger.info("... fetching all songs")
        library = self.mobile.get_all_songs()

        logger.info("... fetching playlist metadata")
        playlists = self.mobile.get_all_playlists()

        logger.info("... fetching playlist contents")
        playlist_contents = self.mobile.get_all_user_playlist_contents()

        logger.info("... fetching uploaded songs")
        uploaded_songs = self.manager.get_uploaded_songs()

        logger.info("... fetching purchased songs")
        purchased_songs = self.manager.get_purchased_songs()

        return Libdata(
            timestamp=datetime.utcnow(),
            registered_devices=registered_devices,
            all_songs=library,
            playlist_metadata=playlists,
            playlists=playlist_contents,
            uploaded_songs=uploaded_songs,
            purchased_songs=purchased_songs
        )

    def get_streamed_song(self, id):
        logger.info("Downloading streamed song id {}".format(id))
        stream_url = self.mobile.get_stream_url(id)
        response = urllib.request.urlopen(stream_url)
        return response.read()

    def get_uploaded_song(self, id):
        logger.info("Downloading uploaded song id {}".format(id))
        suggested_filename, data = self.manager.download_song(id)
        return data
