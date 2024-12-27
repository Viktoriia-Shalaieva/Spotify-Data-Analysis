import os
import yaml
import pandas as pd
from logs.logger_config import logger
from source import utils
from source.api import secrets_functions, spotify
from source.preprocessing import data_prep
from source.web_scraping import chosic


def main():
    BUCKET_NAME = 'project-spotify-analysis-data'

    # Get configs
    config = utils.get_config()
    path_config = utils.get_path_config()

    # Get secrets and API tokens
    spotify_secret = secrets_functions.get_secrets(secret_group='spotify')
    discogs_secret = secrets_functions.get_secrets(secret_group='discogs')

    discogs_api_token = discogs_secret.get('discogs_api_token')

    spotify_api_token = spotify.get_spotify_access_token(
        client_id=spotify_secret['client_id'],
        client_secret=spotify_secret['client_secret']
    )
    # Get playlist names:ids
    playlists_all = config['playlists']

    # Handle paths
    data_dir = path_config['data_dir'][0]
    raw_dir = path_config['raw_dir'][0]
    genres_dir = path_config['genres_dir'][0]
    file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

    playlists_path = str(file_paths['playlists.csv'])
    albums_path = str(file_paths['albums.csv'])
    artists_path = str(file_paths['artists.csv'])
    artists_genres_discogs_path = str(file_paths['artists_genres_discogs.csv'])
    artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
    tracks_path = str(file_paths['tracks.csv'])

    genres_path = os.path.join(genres_dir, 'genres.yaml')

    # Get playlist IDs
    playlists_id = list(playlists_all.values())

    # Check the status of Spotify playlists
    status_codes = spotify.get_playlist_status_code(spotify_api_token, playlists_id)

    if all(code == 200 for code in status_codes):
        logger.info("All status codes are 200. Proceeding with fetching and preprocessing data from Spotify API.")

        # Download  and save playlist data
        playlist_data = spotify.get_save_playlist(spotify_api_token, playlists_all, raw_dir)
        logger.info('Playlist data has been downloaded successfully.')
        playlists_ids = list(playlists_all.values())

        # Preprocess and save playlist data to csv
        playlists_df = data_prep.create_all_playlists_table(
            token=spotify_api_token,
            playlists_id=playlists_ids,
            path=playlists_path,
            save=True)
        logger.info(f'Playlist data has been preprocessed and saved successfully to {playlists_path}.')

        # Get other IDs
        album_ids = set(playlists_df['album_id'])
        artist_ids = set(playlists_df['artist_id'])
        track_ids = set(playlists_df['track_id'])

        # Preprocess and save albums data to csv
        albums_df = data_prep.create_albums_table(
            token=spotify_api_token,
            album_ids=album_ids,
            path=albums_path,
            save=True)
        logger.info(f'Albums data has been preprocessed and saved successfully to {albums_path}.')

        # Preprocess and save tracks data to csv
        tracks_df = data_prep.create_tracks_table(
            token=spotify_api_token,
            track_ids=track_ids,
            path=tracks_path,
            save=True)
        logger.info(f'Tracks data has been preprocessed and saved successfully to {tracks_path}.')

        # Preprocess and save artists data to csv
        artists_df = data_prep.create_artists_table(
            token=spotify_api_token,
            artist_ids=artist_ids,
            path=artists_path,
            save=True)
        logger.info(f'Artists data has been preprocessed and saved successfully to {tracks_path}.')

        # Check for missing artist genres
        empty_genre_count_art = (artists_df['artist_genres'] == '[]').sum()
        logger.info(f"Number of empty artist genres in artists.csv: {empty_genre_count_art}")

        # Get and save artist genres using Discogs API
        artists_genres_discogs = data_prep.create_artist_genre_table(
            token=discogs_api_token,
            file=artists_df,
            path=artists_genres_discogs_path,
            save=True)
        logger.info(
            f"Artist's genres data has been preprocessed and saved successfully to "
            f"{artists_genres_discogs_path}."
        )

        # Check for missing genres in Discogs data
        empty_artists_genres_count = (artists_genres_discogs['artist_genre'] == '[]').sum()
        logger.info(f"Number of empty genres in artists_genres_discogs.csv: {empty_artists_genres_count}")

        # Combine and preprocess artist genres
        artists_df['artist_genres'] = artists_df['artist_genres'].replace('[]', pd.NA)
        artists = artists_df.merge(artists_genres_discogs, on='artist_name', how='left')

        # Fill missing values in the 'artist_genres' column with corresponding values from the 'artist_genre' column.
        artists['artist_genres'] = artists['artist_genres'].fillna(artists['artist_genre'])
        artists = artists.drop(columns=['artist_genre'])
        artists['artist_genres'] = artists['artist_genres'].replace('[]', 'unknown genre')
        artists.to_csv(artists_genres_full_unknown_path, index=False, sep="~")

        # Check for missing genres
        empty_genre_count_art = (artists['artist_genres'] == 'unknown genre').sum()
        logger.info(f"Number of empty artist genres in artists_genres_full_unknown.csv: {empty_genre_count_art}")

        # Upload processed data to S3 bucket
        utils.upload_preprocessed_data_to_s3(bucket_name=BUCKET_NAME)

    else:
        # Download preprocessed data from S3 if API status codes are not all 200
        logger.info("Not all status codes are 200. Downloading preprocessed data from S3 instead.")
        utils.download_preprocessed_data_from_s3(bucket_name=BUCKET_NAME)

    # Get and save genres from Chosic
    genres = chosic.get_genres()
    with open(genres_path, 'w', encoding='utf-8') as file:
        yaml.dump(genres, file, default_flow_style=False, allow_unicode=True)
    utils.upload_chosic_genres_to_s3(bucket_name=BUCKET_NAME)


if __name__ == '__main__':
    main()
