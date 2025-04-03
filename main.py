import tidalapi
import spotify
import time
from os.path import isfile
import pickle
from logzero import logger, logfile

config = tidalapi.Config(quality=tidalapi.Quality.high_lossless, video_quality=tidalapi.VideoQuality.low)
session = tidalapi.Session(config)

if isfile(".tidal_cache"):
    session.load_session_from_file('.tidal_cache')
else:
    session.login_oauth_simple()
    session.save_session_to_file(".tidal_cache")

logfile("conversion.log")


def create_spoti_dump():
    with open("spotify_dump.pkl", "wb") as f:
        pickle.dump(spotify.list_all_playlists(), f)

    print("Spotify dump created!")
    return True


def read_spoti_dump():
    with open("spotify_dump.pkl", "rb") as f:
        return pickle.load(f)


def tidal_to_spotify(session):
    if session.check_login():
        print("Getting list of Spotify playlists...")
        for item in read_spoti_dump():
            time.sleep(5)
            playlist = session.user.create_playlist(item[0], "xD")
            print(f"Creating {playlist.name} on TIDAL...")

            tracks = []

            for trackname in item[2]:
                time.sleep(1.1)
                track = session.search(trackname)

                if track["tracks"]:
                    track = track["tracks"][0]
                else:
                    logger.error(f"Missed song in {item[0]}: {trackname}")
                    continue

                if len(tracks) < 100:
                    tracks.append(str(track.id))
                else:
                    # print(tracks)
                    playlist.add(tracks)
                    # print("Added 100 songs. Waiting a while...")
                    tracks = []
                    time.sleep(5)

            if tracks:
                try:
                    playlist.add(tracks)
                except ValueError:
                    pass

            print(f"Spotify had: {item[1]}, TIDAL has: {len(playlist.tracks())}")
            print(f"{playlist.name}: {playlist.listen_url}")

        print("Conversion finished")


if __name__ == "__main__":
    tidal_to_spotify(session)
