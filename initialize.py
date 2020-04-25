from gmusicapi import Mobileclient

# This only needs to be run once.  Re-use the creds from where it is stored
api = Mobileclient()
api.perform_oauth(storage_filepath="/Users/jd/ws/gmusic/.creds", open_browser=True)


# # after running api.perform_oauth() once:
# api.oauth_login('<a previously-registered device id>')
# # => True
#
# library = api.get_all_songs()
# sweet_track_ids = [track['id'] for track in library
#                    if track['artist'] == 'The Cat Empire']
#
# playlist_id = api.create_playlist('Rad muzak')
# api.add_songs_to_playlist(playlist_id, sweet_track_ids)