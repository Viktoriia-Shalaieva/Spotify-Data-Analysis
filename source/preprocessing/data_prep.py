import pandas as pd
from source.api import discogs
from source.api import spotify
import time
from logs.logger_config import logger


def create_playlist_table(playlist):
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    playlist_followers_total = playlist['followers']['total']
    rows = []

    for item in playlist['tracks']['items']:
        track = item['track']
        track_added_at = item['added_at']

        row = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'playlist_followers_total': playlist_followers_total,
            'track_id': track.get('id'),
            'track_name': track.get('name'),
            'track_added_at': track_added_at,
            'track_duration_ms': track.get('duration_ms'),
            'track_popularity': track.get('popularity'),
            'track_explicit': track.get('explicit'),
            'track_restrictions': track.get('restrictions', {}).get('reason'),
            'track_isrc': track.get('external_ids', {}).get('isrc'),
            'track_ean': track.get('external_ids', {}).get('ids'),
            'track_upc': track.get('external_ids', {}).get('upc'),
        }
        album = track.get('album', {})

        album_info = {
            'album_id': album.get('id'),
            'album_name': album.get('name'),
            'album_release_date': album.get('release_date'),
            'album_type': album.get('album_type'),
            'album_total_tracks': album.get('total_tracks'),
            'album_restrictions': album.get('restrictions', {}).get('reason'),
        }
        artists_info = {
            'artist_id': ', '.join([artist.get('id') for artist in track.get('artists', [])]),
            'artist_name': ', '.join([artist.get('name') for artist in track.get('artists', [])]),
        }
        row.update(album_info)
        row.update(artists_info)

        rows.append(row)
    df = pd.DataFrame(rows)
    logger.info(f"Playlist '{playlist_name}' processed with {len(rows)} tracks.")
    return df


def create_all_playlists_table(token, playlists_id):
    all_playlists = []
    for playlist_id in playlists_id:
        playlist_data = spotify.get_playlist(token, playlist_id)
        logger.info(f"Retrieving playlist data for playlist ID: {playlist_id}")
        time.sleep(1)
        df_playlist = create_playlist_table(playlist_data)
        all_playlists.append(df_playlist)

    playlists = pd.concat(all_playlists, ignore_index=True)
    logger.info("All playlists processed successfully.")
    return playlists


def create_tracks_table(access_token, track_ids):
    tracks_data = []

    for track_id in track_ids:
        track_info = spotify.get_track(access_token, track_id)
        time.sleep(1)

        if track_info:
            track_data = {
                'track_id': track_info.get('id'),
                'track_name': track_info.get('name'),
                'track_duration_ms': track_info.get('duration_ms'),
                'track_explicit': track_info.get('explicit'),
                'track_popularity': track_info.get('popularity'),
                'track_restrictions': track_info.get('restrictions', {}).get('reason')
            }
            tracks_data.append(track_data)
            logger.info(f"Track data retrieved successfully for track ID: {track_id}")
        else:
            logger.error(f"Track data not found for track ID: {track_id}")

    tracks = pd.DataFrame(tracks_data)
    logger.info("All track data processed successfully.")
    return tracks


def create_albums_table(access_token, album_ids):
    albums_data = []

    for album_id in album_ids:
        album_info = spotify.get_album(access_token, album_id)
        time.sleep(1)

        if album_info:
            album_data = {
                'album_id': album_info.get('id'),
                'album_name': album_info.get('name'),
                'album_type': album_info.get('album_type'),
                'album_release_date': album_info.get('release_date'),
                'album_total_tracks': album_info.get('total_tracks'),
                'album_genres': album_info.get('genres'),
                'album_label': album_info.get('label'),
                'album_popularity': album_info.get('popularity'),
                'album_restrictions': album_info.get('restrictions', {}).get('reason'),
            }
            albums_data.append(album_data)
            logger.info(f"Album data retrieved successfully for album ID: {album_id}")
        else:
            logger.error(f"Album data not found for album ID: {album_id}")

    albums = pd.DataFrame(albums_data)
    logger.info("All album data processed successfully.")
    return albums


def create_tracks_af_table(access_token, track_ids):
    rows = []

    for track_id in track_ids:
        track_info = spotify.get_track_audio_features(access_token, track_id)
        time.sleep(1)

        if track_info:
            row = {
                'track_id': track_info.get('id'),
                'track_acousticness': track_info.get('acousticness'),
                'track_danceability': track_info.get('danceability'),
                'track_duration_ms': track_info.get('duration_ms'),
                'track_energy': track_info.get('energy'),
                'track_instrumentalness': track_info.get('instrumentalness'),
                'track_key': track_info.get('key'),
                'track_liveness': track_info.get('liveness'),
                'track_loudness': track_info.get('loudness'),
                'track_mode': track_info.get('mode'),
                'track_speechiness': track_info.get('speechiness'),
                'track_tempo': track_info.get('tempo'),
                'track_time_signature': track_info.get('time_signature'),
                'track_valence': track_info.get('valence'),
            }
            rows.append(row)
            logger.info(f"Audio features retrieved for track ID: {track_id}")
        else:
            logger.error(f"Audio features not found for track ID: {track_id}")

    tracks_af = pd.DataFrame(rows)
    return tracks_af


def create_artists_table(access_token, artist_ids):
    rows = []
    unique_artist_ids = set()

    for ids in artist_ids:
        separated_ids = [artist.strip() for artist in ids.split(',')]
        unique_artist_ids.update(separated_ids)

    for artist_id in unique_artist_ids:
        artist_info = spotify.get_artist(access_token, artist_id)
        time.sleep(1)

        if artist_info:
            row = {
                'artist_id': artist_info.get('id'),
                'artist_name': artist_info.get('name'),
                'artist_followers': artist_info.get('followers', {}).get('total'),
                'artist_genres': artist_info.get('genres'),
                'artist_popularity': artist_info.get('popularity'),
            }
            rows.append(row)
            logger.info(f"Artist data retrieved for artist ID: {artist_id}")
        else:
            logger.error(f"Artist data not found for artist ID: {artist_id}")

    artists = pd.DataFrame(rows)
    logger.info("All artist data processed successfully.")
    return artists


def create_track_genre_table(file, discogs_api_token):
    rows = []

    for _, row in file.iterrows():  # Using _ indicates that the index value is not important and will not be used.
        track_id = row['track_id']
        track_name = row['track_name']
        artists = row['artist_name']

        genres = discogs.get_genre(discogs_api_token, track_name, artists)
        time.sleep(1)

        rows.append({
                'track_id': track_id,
                'track_name': track_name,
                'artist_name': artists,
                'track_genre': genres,
        })
        logger.info(f"Genre data retrieved for track '{track_name}' by artist '{artists}'")

    track_genre = pd.DataFrame(rows, columns=['track_id', 'track_name', 'artist_name', 'track_genre'])
    logger.info("All track genre data processed successfully.")
    return track_genre


def create_artist_genre_table(file, discogs_api_token):
    rows = []

    for _, row in file.iterrows():  # Using _ indicates that the index value is not important and will not be used.
        artist_id = row['artist_id']
        artist = row['artist_name']

        genres = discogs.get_genre_artist(discogs_api_token, artist)
        time.sleep(1)

        rows.append({
                'artist_id': artist_id,
                'artist_name': artist,
                'artist_genre': genres,
        })
        logger.info(f"Genre data retrieved for artist '{artist}'")
    artist_genre = pd.DataFrame(rows, columns=['artist_id', 'artist_name', 'artist_genre'])
    logger.info("All artist genre data processed successfully.")
    return artist_genre
