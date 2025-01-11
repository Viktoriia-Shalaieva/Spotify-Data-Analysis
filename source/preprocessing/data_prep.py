import random
import time

import pandas as pd

from logs.logger_config import logger
from source.api import discogs, spotify


def create_playlist_table(playlist):
    """
    Extracts data from a Spotify playlist, including playlist details (ID, name, followers, country) and track-specific
    information (track ID, album ID, artist IDs). The results are returned as a pandas DataFrame.
    """
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
    """
    Retrieve data for multiple Spotify playlists, processes each playlist
    using `create_playlist_table`, and concatenates the results into a single DataFrame.

    Args:
        token (str): Spotify API token for authentication.
        playlists_id (list of str): A list of playlist IDs to retrieve and process.
        path (str): File path to save the resulting DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the combined DataFrame to a CSV file. Defaults to False.
    """
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
    """
    Retrieve data for multiple Spotify tracks, process each track,
    and concatenate the results into a single DataFrame.

    Args:
        token (str): Spotify API token for authentication.
        track_ids (list of str): A list of track IDs to retrieve and process.
        path (str): File path to save the resulting DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the combined DataFrame to a CSV file. Defaults to False.
    """
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
    """
    Retrieve data for multiple Spotify albums, process each album,
    and concatenate the results into a single DataFrame.

    Args:
        token (str): Spotify API token for authentication.
        album_ids (list of str): A list of album IDs to retrieve and process.
        path (str): File path to save the resulting DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the combined DataFrame to a CSV file. Defaults to False.
    """
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
    """
    Retrieve data for multiple Spotify artists, process each artist,
    and concatenate the results into a single DataFrame.

    Args:
        token (str): Spotify API token for authentication.
        artist_ids (list of str): A list of artist IDs or comma-separated strings of artist IDs to retrieve and process.
        path (str): File path to save the resulting DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the combined DataFrame to a CSV file. Defaults to False.
    """
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
    """
    Retrieve genre data for multiple artists and create a DataFrame.

    This function processes a file containing artist names, retrieves genre data for each artist,
    and creates a DataFrame with the results. Optionally, the DataFrame can be saved as a CSV file.

    Args:
        token (str): Discogs API token for authentication.
        file (pd.DataFrame): A DataFrame containing artist information. It must include a column named 'artist_name'.
        path (str): File path to save the resulting DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the resulting DataFrame to a CSV file. Defaults to False.
    """
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


def process_artist_genres(artists_df, path, save):
    """
    Processes the 'artist_genres' column in a DataFrame, replacing missing genres
    with randomly generated genres based on the distribution of existing genres.

    Args:
        artists_df (pd.DataFrame): A DataFrame containing artist information.
            It must include a column named 'artist_genres'.
        path (str): File path to save the processed DataFrame as a CSV file if `save` is True.
        save (bool): Whether to save the processed DataFrame to a CSV file. Defaults to False.

    """
    # Replace empty lists ('[]') with NaN
    artists_df['artist_genres'] = artists_df['artist_genres'].replace('[]', pd.NA)

    # Remove square brackets and extra quotes
    artists_df['artist_genres'] = (
        artists_df['artist_genres']
        .str.strip("[]")
        .str.replace("'", "")
    )
    # Count the frequency of each genre
    genre_counts = artists_df['artist_genres'].str.split(', ').explode().value_counts()

    genres_list = genre_counts.index.tolist()
    weights = genre_counts.tolist()

    unknown_genre_indices = artists_df[artists_df['artist_genres'].isna()].index

    # Generate random genres for missing values based on frequency distribution
    random_genres = random.choices(
        population=genres_list,
        weights=weights,
        k=len(unknown_genre_indices)
    )

    # Assign the generated random genres to missing values
    artists_df.loc[unknown_genre_indices, 'artist_genres'] = random_genres

    if save:
        artists_df.to_csv(path, index=False, sep="~")

    return artists_df
