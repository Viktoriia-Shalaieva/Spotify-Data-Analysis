import yaml
from source.api import s3_functions
from slugify import slugify
from logs.logger_config import logger


def load_config(config_path, encoding='utf-8'):
    """Load a YAML configuration file."""
    with open(config_path, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)


# def get_secrets(secret_group):
#     # with open('.credentials.yaml', 'r') as file:
#     #     credentials = yaml.safe_load(file)
#     credentials = load_config('.credentials.yaml')
#
#     secrets = credentials.get(secret_group)
#
#     return secrets


# def get_config():
#     with open('config/config.yaml', 'r') as file:
#         config = yaml.safe_load(file)
#
#     return config
#
#
# def get_path_config():
#     with open('config/path_config.yaml', 'r') as config_file:
#         path_config = yaml.safe_load(config_file)
#
#     return path_config


# def upload_preprocessed_data_to_s3(bucket_name):
#     s3_functions.upload_to_s3(
#         file_name="data/preprocessed/albums.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/albums.csv")
#
#     s3_functions.upload_to_s3(
#         file_name="data/preprocessed/artists_full.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/artists_full.csv")
#
#     s3_functions.upload_to_s3(
#         file_name="data/preprocessed/playlists.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/playlists.csv")
#
#     s3_functions.upload_to_s3(
#         file_name="data/preprocessed/tracks.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/tracks.csv")
#
#     return None
#
#
# def download_preprocessed_data_from_s3(bucket_name):
#     s3_functions.download_from_s3(
#         file_name="data/preprocessed/albums.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/albums.csv")
#
#     s3_functions.download_from_s3(
#         file_name="data/preprocessed/artists_full.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/artists_full.csv")
#
#     s3_functions.download_from_s3(
#         file_name="data/preprocessed/playlists.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/playlists.csv")
#
#     s3_functions.download_from_s3(
#         file_name="data/preprocessed/tracks.csv",
#         bucket_name=bucket_name,
#         s3_key="data/preprocessed/tracks.csv")
#
#     return None


def get_s3_file_paths(file_type, config_path='config/s3_files.yaml'):
    config = load_config(config_path)
    return config.get(file_type, [])


# def upload_preprocessed_data_to_s3(bucket_name, file_type, config_path='config/s3_files.yaml'):
#     file_paths = get_s3_file_paths(file_type, config_path)
#     for file_path in file_paths:
#         s3_functions.upload_to_s3(
#             file_name=file_path,
#             bucket_name=bucket_name,
#             s3_key=file_path
#         )
#
#
# def download_preprocessed_data_from_s3(bucket_name, file_type, config_path='config/s3_files.yaml'):
#     file_paths = get_s3_file_paths(file_type, config_path)
#     for file_path in file_paths:
#         s3_functions.download_from_s3(
#             file_name=file_path,
#             bucket_name=bucket_name,
#             s3_key=file_path
#         )


# def upload_chosic_genres_to_s3(bucket_name,config_path='config/s3_files.yaml', file_type='genre_files'):
#     file_paths = get_s3_file_paths(file_type, config_path)
#     s3_functions.upload_to_s3(
#         file_name=file_type,
#         bucket_name=bucket_name,
#         s3_key=file_type)
#
#     return None


# def upload_raw_playlists_to_s3(bucket_name, config_path='config/config.yaml'):
#     config = load_config(config_path)
#
#     playlist_files = []
#     for playlist_name in config['playlists'].keys():
#         file_name = f"data/raw/playlists/{slugify(playlist_name, separator='_')}.json"
#         playlist_files.append({
#             "file_name": file_name,
#             "s3_key": file_name
#         })
#
#     # s3_functions.upload_files_to_s3(bucket_name, playlist_files)
#     for file in playlist_files:
#         s3_functions.upload_to_s3(
#             file_name=file["file_name"],
#             bucket_name=bucket_name,
#             s3_key=file["s3_key"]
#         )
#
#
# def download_raw_playlists_from_s3(bucket_name, config_path='config/config.yaml'):
#     config = load_config(config_path)
#
#     playlist_files = []
#     for playlist_name in config['playlists'].keys():
#         file_name = f"data/raw/playlists/{slugify(playlist_name, separator='_')}.json"
#         playlist_files.append({
#             "file_name": file_name,
#             "s3_key": file_name
#         })
#
#     for file in playlist_files:
#         s3_functions.download_from_s3(
#             file_name=file["file_name"],
#             bucket_name=bucket_name,
#             s3_key=file["s3_key"]
#         )
def sync_preprocessed_data_with_s3(bucket_name, operation, file_type, config_path='config/s3_files.yaml'):
    """
    Synchronize preprocessed data files with S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        operation (str): The operation to perform ('upload' or 'download').
        file_type (str): The type of file to synchronize ('preprocessed_files' or 'genre_files').
        config_path (str): Path to the configuration file containing file paths (default: 'config/s3_files.yaml').
    """
    if operation not in ['upload', 'download']:
        logger.error(f"Invalid operation: {operation}. Must be 'upload' or 'download'.")
        return

    config = load_config(config_path)

    if file_type not in config:
        logger.error(f"Invalid file type: {file_type}. Must be one of: {', '.join(config.keys())}")
        return

    file_paths = config[file_type]

    logger.info(f"Starting {operation} operation for bucket: {bucket_name}")
    for file_path in file_paths:
        if operation == 'upload':
            s3_functions.upload_to_s3(
                file_name=file_path,
                bucket_name=bucket_name,
                s3_key=file_path
            )
        elif operation == 'download':
            s3_functions.download_from_s3(
                file_name=file_path,
                bucket_name=bucket_name,
                s3_key=file_path
            )

    logger.info(f"{operation.capitalize()} operation completed successfully for bucket: {bucket_name}")


def sync_raw_playlists_with_s3(bucket_name, operation, config_path='config/config.yaml'):
    """
    Synchronize raw playlist files with S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        operation (str): The operation to perform ('upload' or 'download').
        config_path (str): Path to the configuration file (default: 'config/config.yaml').
    """
    if operation not in ['upload', 'download']:
        logger.error(f"Invalid operation: {operation}. Must be 'upload' or 'download'.")
        return

    logger.info(f"Loading configuration from: {config_path}")
    config = load_config(config_path)

    playlist_files = []
    for playlist_name in config['playlists'].keys():
        file_name = f"data/raw/playlists/{slugify(playlist_name, separator='_')}.json"
        playlist_files.append({
            "file_name": file_name,
            "s3_key": file_name
        })

    logger.info(f"Starting {operation} operation for bucket: {bucket_name}")
    for file in playlist_files:
        if operation == 'upload':
            s3_functions.upload_to_s3(
                file_name=file["file_name"],
                bucket_name=bucket_name,
                s3_key=file["s3_key"]
            )
        elif operation == 'download':
            s3_functions.download_from_s3(
                file_name=file["file_name"],
                bucket_name=bucket_name,
                s3_key=file["s3_key"]
            )

    logger.info(f"{operation.capitalize()} operation completed successfully for bucket: {bucket_name}")
