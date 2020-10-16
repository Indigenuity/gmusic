import os


class Libdata:

    def __init__(self,
                 id,
                 registered_devices,
                 all_songs,
                 playlist_metadata,
                 playlists,
                 uploaded_songs,
                 purchased_songs):
        self.id = id
        self.registered_devices = registered_devices
        self.all_songs = all_songs
        self.playlist_metadata = playlist_metadata
        self.playlists = playlists
        self.uploaded_songs = uploaded_songs
        self.purchased_songs = purchased_songs
