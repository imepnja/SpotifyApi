import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import random

def dump(item):
    print(json.dumps(item, indent=4))

def main() :
    client_id = '4e8dd866d911492381aa44f4770f25f2'
    client_secret = 'b481ff45717b435b837a8bdfdc947c74'


    sp_user_libary = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri='http://localhost',
                                                scope="playlist-modify-public user-library-read"
                                                ))
    updateNewLikesPlaylist(sp_user_libary)

def getTrackURIFromPlaylist(id, sp, count):

    playlist = []
    offset = 0

    while count > 100: # requests up to 100 possible
        playlist.extend(sp.playlist_items(id, fields=None, limit=count, offset=offset)['items'])
        offset += 100
        count -= 100

    playlist.extend(sp.playlist_items(id, fields=None, limit=count, offset=offset)['items'])
    
    list = []
    for i, x in enumerate(playlist):
        print(x['track']['name'])
        list.append(x['track']['uri'])
    return list

def getTrackURIFromSaved(sp, count, offset=0):
    last_liked_songs = []
    
    while count > 50: # requests up to 50 only possible
        last_liked_songs.extend(sp.current_user_saved_tracks(limit=50, offset=offset)['items'])
        count -= 50
        offset += 50


    last_liked_songs.extend(sp.current_user_saved_tracks(limit=count, offset=offset)['items'])

    list = []
    for i, x in enumerate(last_liked_songs):
        print(x['track']['name'])
        list.append(x['track']['uri'])
    return list




def updateNewLikesPlaylist(sp):
    ################

    # ratios:
    recent_likes_count = 50
    on_repeat_count = 15
    repeat_rewind_count = 20
    some_saved_count = 50

    # other information:

    saved_songs_count = 757

    new_likes_playlist_uri = 'spotify:playlist:4MikSpVwFB9RHu0y6LPS2i'
    on_repeat_uir = 'spotify:playlist:37i9dQZF1EpjlHHP2gAsaD'
    repeat_rewind_uri = 'spotify:playlist:37i9dQZF1EpAyu4Yzt2ExR'

    ################ 
    
    new_likes_playlist_uri = input('New playlist uri (rightclick on playlist -> Share -> Copy Spotify URI: ')





    new_playlist = []

    recent_saved_tracks = getTrackURIFromSaved(sp, recent_likes_count)
    on_repeat_tracks = getTrackURIFromPlaylist(on_repeat_uir, sp, 30)
    repeat_rewind_tracks = getTrackURIFromPlaylist(repeat_rewind_uri, sp, 30)

    all_saved_tracks = getTrackURIFromSaved(sp, saved_songs_count)
    
    # shuffeling playlists
    random.shuffle(on_repeat_tracks)
    random.shuffle(repeat_rewind_tracks)
    random.shuffle(all_saved_tracks)

    new_playlist.extend(recent_saved_tracks)
    new_playlist.extend(on_repeat_tracks[:on_repeat_count])
    new_playlist.extend(repeat_rewind_tracks[:repeat_rewind_count])
    new_playlist.extend(all_saved_tracks[:some_saved_count])


    random.shuffle(new_playlist)


    ### Reset Playlist and place new Tracks
    offset = len(new_playlist) -1
    sp.playlist_replace_items(new_likes_playlist_uri, [])
    while offset > 100:
        sp.playlist_add_items(new_likes_playlist_uri, new_playlist[offset-100:offset])
        offset -= 100
    sp.playlist_add_items(new_likes_playlist_uri, new_playlist[:offset+1])
    




if __name__ == "__main__":
    main()

