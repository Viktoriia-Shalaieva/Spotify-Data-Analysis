import pandas as pd
from source.api.spotify import *


def create_playlist(playlist):
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
            'track_id': track['id'],
            'track_name': track['name'],
            'track_added_at': track_added_at,
            'track_duration_ms': track['duration_ms'],
            'track_popularity': track['popularity'],
            'track_explicit': track['explicit'],
            'track_restrictions': track.get('restrictions', {}).get('reason'),
            'track_isrc': track['external_ids'].get('isrc'),
            'track_ean': track['external_ids'].get('ids'),
            'track_upc': track['external_ids'].get('upc'),
        }

        album = track['album']

        album_info = {
            'album_id': album['id'],
            'album_name': album['name'],
            'album_release_date': album['release_date'],
            'album_type': album['album_type'],
            'album_total_tracks': album['total_tracks'],
            'album_restrictions': album.get('restrictions', {}).get('reason'),
        }

        artists_info = {
            'artist_id': ', '.join([artist['id'] for artist in track['artists']]),
            'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
        }

        row.update(album_info)
        row.update(artists_info)

        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def create_all_playlists(token, playlists_id):
    all_playlists = []
    for playlist_id in playlists_id:
        playlist_data = get_playlist(token, playlist_id)
        df_playlist = create_playlist(playlist_data)
        all_playlists.append(df_playlist)

    playlists = pd.concat(all_playlists, ignore_index=True)
    return playlists
