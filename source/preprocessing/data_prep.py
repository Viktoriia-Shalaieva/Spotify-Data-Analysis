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
