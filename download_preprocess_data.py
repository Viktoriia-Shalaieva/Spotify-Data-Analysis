import pandas as pd
import yaml
import os
from source.api import spotify
from source.web_scraping import chosic
from source.preprocessing import data_prep
from logs.logger_config import logger
from source import utils


def main():
    BUCKET_NAME = 'project-spotify-analysis-data'

    # get configs
    config = utils.get_config()
    path_config = utils.get_path_config()


    # get secrets
    spotify_secret = utils.get_secrets(secret_group='spotify')
    discogs_secret = utils.get_secrets(secret_group='discogs')
    discogs_api_token = discogs_secret.get('discogs_api_token')

    spotify_api_token = spotify.get_spotify_access_token(
        client_id=spotify_secret['client_id'],
        client_secret=spotify_secret['client_secret']
    )
    # get playlist names:ids
    playlists_all = config['playlists']

    # handle paths
    data_dir = path_config['data_dir'][0]
    raw_dir = path_config['raw_dir'][0]
    genres_dir = path_config['genres_dir'][0]
    file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

    playlists_path = str(file_paths['playlists.csv'])
    albums_path = str(file_paths['albums.csv'])
    artists_path = str(file_paths['artists.csv'])
    artists_genres_discogs_path = str(file_paths['artists_genres_discogs.csv'])
    artists_genres_full_path = str(file_paths['artists_genres_full.csv'])
    artists_genres_full_random_path = str(file_paths['artists_genres_full_random.csv'])
    artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
    tracks_path = str(file_paths['tracks.csv'])

    genres_path = os.path.join(genres_dir, 'genres.yaml')

    playlists_id = list(playlists_all.values())
    # spotify.get_playlist_status_code(spotify_api_token, playlists_id)

    status_codes = spotify.get_playlist_status_code(spotify_api_token, playlists_id)

    if all(code == 200 for code in status_codes):
        logger.info("All status codes are 200. Proceeding with fetching and preprocessing data from Spotify API.")

        # download playlist data
        playlist_data = spotify.get_save_playlist(spotify_api_token, playlists_all, raw_dir)
        logger.info('Playlist data has been downloaded successfully.')
        playlists_ids = list(playlists_all.values())
        # preprocess playlist data
        playlists_df = data_prep.create_all_playlists_table(spotify_api_token, playlists_ids)
        logger.info('Playlist data has been preprocessed successfully.')
        # save playlist data to csv
        playlists_df.to_csv(playlists_path, index=False, sep="~")
        logger.info(f"Playlists data saved to {playlists_path}")

        # get other ids
        album_ids = set(playlists_df['album_id'])
        artist_ids = set(playlists_df['artist_id'])
        track_ids = set(playlists_df['track_id'])

        # handle albums
        albums_df = data_prep.create_albums_table(spotify_api_token, album_ids)
        albums_df.to_csv(albums_path, index=False, sep="~")
        logger.info(f"Albums data saved to {albums_path}")

        # handle tracks
        tracks_df = data_prep.create_tracks_table(spotify_api_token, track_ids)
        tracks_df.to_csv(tracks_path, index=False, sep="~")
        logger.info(f"Tracks data saved to {tracks_path}")

        # handle artists
        artists_df = data_prep.create_artists_table(spotify_api_token, artist_ids)
        artists_df.to_csv(artists_path, index=False, sep="~")
        logger.info(f"Artists data saved to {artists_path}")

        empty_genre_count_art = (artists_df['artist_genres'] == '[]').sum()
        logger.info(f"Number of empty artist genres in artists.csv: {empty_genre_count_art}")

        artists_genres_discogs = data_prep.create_artist_genre_table(artists_df, discogs_api_token)
        artists_genres_discogs.to_csv(artists_genres_discogs_path, index=False, sep="~")

        empty_artists_genres_count = (artists_genres_discogs['artist_genre'] == '[]').sum()
        logger.info(f"Number of empty genres in artists_genres_discogs.csv: {empty_artists_genres_count}")

        artists_df['artist_genres'] = artists_df['artist_genres'].replace('[]', pd.NA)

        artists = artists_df.merge(artists_genres_discogs, on='artist_name', how='left')
        logger.debug(artists)
        artists['artist_genres'] = artists['artist_genres'].fillna(artists['artist_genre'])
        artists = artists.drop(columns=['artist_genre'])
        artists['artist_genres'] = artists['artist_genres'].replace('[]', 'unknown genre')
        artists.to_csv(artists_genres_full_unknown_path, index=False, sep="~")

        empty_genre_count_art = (artists['artist_genres'] == 'unknown genre').sum()
        logger.info(f"Number of empty artist genres in artists_genre_full.csv: {empty_genre_count_art}")

        utils.upload_preprocessed_data_to_s3(bucket_name=BUCKET_NAME)

    else:
        logger.info("Not all status codes are 200. Downloading preprocessed data from S3 instead.")
        utils.download_preprocessed_data_from_s3(bucket_name=BUCKET_NAME)

    genres = chosic.get_genres()
    with open(genres_path, 'w', encoding='utf-8') as file:
        yaml.dump(genres, file, default_flow_style=False, allow_unicode=True)
    utils.upload_chosic_genres_to_s3(bucket_name=BUCKET_NAME)


if __name__ == '__main__':
    main()
