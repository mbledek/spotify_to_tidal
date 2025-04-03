import pathlib
import os
import spotipy

path = pathlib.Path(__file__).parent.absolute()


scopes = "app-remote-control user-modify-playback-state user-read-playback-state user-library-modify streaming " \
         "user-top-read"

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''

# Login to Spotify API
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                              client_secret=SPOTIPY_CLIENT_SECRET,
                                                              redirect_uri="https://example.com/callback",
                                                              scope=scopes,
                                                              open_browser=False,
                                                              cache_path=os.path.join(path, ".cache")))


def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for i in range(len(tracks)):
        try:
            tracks[i] = tracks[i]["track"]["name"] + " " + tracks[i]["track"]["artists"][0]["name"]
        except TypeError:
            pass

    return tracks


def list_all_playlists():
    output_list = []
    playlists = sp.user_playlists('')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist["owner"]["display_name"] == "":
                current_name = playlist["name"]
                print(current_name + " " + playlist["id"])
                list_tracknames = get_playlist_tracks(playlist["id"])
                output_list.append([current_name, len(list_tracknames), list_tracknames])

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    print("List created")
    return output_list
