import time
import pandas as pd
from logs.logger_config import logger
from source.api import discogs, spotify


def create_playlist_table(playlist):
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    playlist_followers_total = playlist['followers']['total']
    country = playlist_name.split('-')[-1].strip()

    rows = []

    for item in playlist['tracks']['items']:
        track = item['track']

        row = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'country': country,
            'playlist_followers_total': playlist_followers_total,
            'track_id': track.get('id'),
        }
        album = track.get('album', {})

        album_info = {
            'album_id': album.get('id'),
        }
        artists_info = {
            'artist_id': ', '.join([artist.get('id') for artist in track.get('artists', [])]),
        }
        row.update(album_info)
        row.update(artists_info)

        rows.append(row)
    df = pd.DataFrame(rows)
    logger.info(f"Playlist '{playlist_name}' processed with {len(rows)} tracks.")

    return df


def create_all_playlists_table(token, playlists_id, path, save):
    all_playlists = []
    for playlist_id in playlists_id:
        playlist_data = spotify.get_playlist(token, playlist_id)
        logger.info(f"Retrieving playlist data for playlist ID: {playlist_id}")
        df_playlist = create_playlist_table(playlist_data)
        all_playlists.append(df_playlist)

    playlists = pd.concat(all_playlists, ignore_index=True)
    logger.info("All playlists processed successfully.")

    if save:
        playlists.to_csv(path, index=False, sep="~")
    return playlists


def create_tracks_table(token, track_ids, path, save):
    tracks_data = []

    for track_id in track_ids:
        track_info = spotify.get_track(token, track_id)
        time.sleep(0.4)

        if track_info:
            track_data = {
                'track_id': track_info.get('id'),
                'track_name': track_info.get('name'),
                'track_duration_ms': track_info.get('duration_ms'),
                'track_explicit': track_info.get('explicit'),
                'track_popularity': track_info.get('popularity'),
            }
            tracks_data.append(track_data)
            logger.info(f"Track data retrieved successfully for track ID: {track_id}")
        else:
            logger.error(f"Track data not found for track ID: {track_id}")

    tracks = pd.DataFrame(tracks_data)
    logger.info("All track data processed successfully.")
    if save:
        tracks.to_csv(path, index=False, sep="~")
    return tracks


def create_albums_table(token, album_ids, path, save):
    albums_data = []

    for album_id in album_ids:
        album_info = spotify.get_album(token, album_id)
        time.sleep(0.4)

        if album_info:
            album_data = {
                'album_id': album_info.get('id'),
                'album_name': album_info.get('name'),
                'album_type': album_info.get('album_type'),
                'album_release_date': album_info.get('release_date'),
                'album_total_tracks': album_info.get('total_tracks'),
                'album_label': album_info.get('label'),
                'album_popularity': album_info.get('popularity'),
            }
            albums_data.append(album_data)
            logger.info(f"Album data retrieved successfully for album ID: {album_id}")
        else:
            logger.error(f"Album data not found for album ID: {album_id}")

    albums = pd.DataFrame(albums_data)
    logger.info("All album data processed successfully.")
    if save:
        albums.to_csv(path, index=False, sep="~")
    return albums


def create_artists_table(token, artist_ids, path, save):
    rows = []
    unique_artist_ids = set()

    for ids in artist_ids:
        separated_ids = [artist.strip() for artist in ids.split(',')]
        unique_artist_ids.update(separated_ids)

    for artist_id in unique_artist_ids:
        artist_info = spotify.get_artist(token, artist_id)
        time.sleep(0.4)

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
    if save:
        artists.to_csv(path, index=False, sep="~")
    return artists


def create_artist_genre_table(token, file, path, save):
    rows = []

    for _, row in file.iterrows():  # Using _ indicates that the index value is not important and will not be used.
        artist = row['artist_name']

        genres = discogs.get_genre_artist(token, artist)
        time.sleep(0.7)

        rows.append({
                'artist_name': artist,
                'artist_genre': genres,
        })
        logger.info(f"Genre data retrieved for artist '{artist}'")
    artist_genre = pd.DataFrame(rows, columns=['artist_name', 'artist_genre'])
    logger.info("All artist genre data processed successfully.")
    if save:
        artist_genre.to_csv(path, index=False, sep="~")
    return artist_genre
