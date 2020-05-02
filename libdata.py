import os


class Libdata:

    def __init__(self,
                 registered_devices,
                 all_songs,
                 playlist_metadata,
                 playlists):
        self.registered_devices = registered_devices
        self.all_songs = all_songs
        self.playlist_metadata = playlist_metadata
        self.playlists = playlists
