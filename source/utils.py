import yaml
from source.api import s3_functions


def get_secrets(secret_group):
    with open('.credentials.yaml', 'r') as file:
        credentials = yaml.safe_load(file)

    secrets = credentials.get(secret_group)

    return secrets


def get_config():
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    return config


def get_path_config():
    with open('config/path_config.yaml', 'r') as config_file:
        path_config = yaml.safe_load(config_file)

    return path_config


def upload_preprocessed_data_to_s3(bucket_name):
    s3_functions.upload_to_s3(
        file_name="data/preprocessed/albums.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/albums.csv")

    s3_functions.upload_to_s3(
        file_name="data/preprocessed/artists_genres_full_unknown.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/artists_genres_full_unknown.csv")

    s3_functions.upload_to_s3(
        file_name="data/preprocessed/playlists.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/playlists.csv")

    s3_functions.upload_to_s3(
        file_name="data/preprocessed/tracks.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/tracks.csv")

    return None


def download_preprocessed_data_from_s3(bucket_name):
    s3_functions.download_from_s3(
        file_name="data/preprocessed/albums.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/albums.csv")

    s3_functions.download_from_s3(
        file_name="data/preprocessed/artists_genres_full_unknown.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/artists_genres_full_unknown.csv")

    s3_functions.download_from_s3(
        file_name="data/preprocessed/playlists.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/playlists.csv")

    s3_functions.download_from_s3(
        file_name="data/preprocessed/tracks.csv",
        bucket_name=bucket_name,
        s3_key="data/preprocessed/tracks.csv")

    return None

def upload_chosic_genres_to_s3(bucket_name):
    s3_functions.upload_to_s3(
        file_name="data/genres/genres.yaml",
        bucket_name=bucket_name,
        s3_key="data/genres/genres.yaml")

    return None

