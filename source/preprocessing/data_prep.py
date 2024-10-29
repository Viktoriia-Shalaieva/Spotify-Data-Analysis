import pandas as pd
from source.api.spotify import *


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
    return df


def create_all_playlists_table(token, playlists_id):
    all_playlists = []
    for playlist_id in playlists_id:
        playlist_data = get_playlist(token, playlist_id)
        df_playlist = create_playlist_table(playlist_data)
        all_playlists.append(df_playlist)

    playlists = pd.concat(all_playlists, ignore_index=True)
    return playlists


def create_tracks_table(access_token, track_ids):
    tracks_data = []

    for track_id in track_ids:
        track_info = get_track(access_token, track_id)

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

    tracks = pd.DataFrame(tracks_data)
    return tracks


def create_albums_table(access_token, album_ids):
    albums_data = []

    for album_id in album_ids:
        album_info = get_album(access_token, album_id)

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

    albums = pd.DataFrame(albums_data)
    return albums


def create_tracks_af_table(access_token, track_ids):
    tracks_af_data = []

    for track_id in track_ids:
        track_info = get_track_audio_features(access_token, track_id)

        if track_info:
            track_data = {
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
            tracks_af_data.append(track_data)

    tracks_af = pd.DataFrame(tracks_af_data)
    return tracks_af
