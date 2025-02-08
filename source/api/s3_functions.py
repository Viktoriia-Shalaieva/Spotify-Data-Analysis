import os

import boto3
from slugify import slugify

from logs.logger_config import logger
from source.api import secrets_functions
from source import utils


aws_secrets = secrets_functions.get_secrets("aws")

# Create S3 resource
s3 = boto3.resource(
   service_name="s3",
   region_name="eu-central-1",
   aws_access_key_id=aws_secrets.get("aws_access_key_id"),
   aws_secret_access_key=aws_secrets.get("aws_secret_access_key"),
)


def upload_to_s3(file_name, bucket_name, s3_key):
    """Upload a file to an Amazon S3 bucket."""
    try:
        s3.Bucket(bucket_name).upload_file(Filename=file_name, Key=s3_key)
        logger.info(f"'{file_name}' has been uploaded to bucket '{bucket_name}' as '{s3_key}'.")
    except Exception as e:
        logger.error(f"Error uploading file: {e}")


def download_from_s3(file_name, bucket_name, s3_key):
    directory = os.path.dirname(file_name)
    os.makedirs(directory, exist_ok=True)
    try:
        s3.Bucket(bucket_name).download_file(Filename=file_name, Key=s3_key)
        logger.info(f"File '{s3_key}' has been downloaded from bucket '{bucket_name}' to local path '{file_name}'.")
    except Exception as e:
        logger.error(f"Error downloading file: {e}")


# def get_s3_file_paths(file_type, config_path="config/s3_files.yaml"):
#     config = utils.load_config(config_path)
#     return config.get(file_type, [])


def sync_preprocessed_data_with_s3(bucket_name, operation, file_type, config_path="config/s3_files.yaml"):
    """
    Synchronize preprocessed data files with S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        operation (str): The operation to perform ("upload" or "download").
        file_type (str): The type of file to synchronize ("preprocessed_files" or "genre_files").
        config_path (str): Path to the configuration file containing file paths (default: "config/s3_files.yaml").
    """
    if operation not in ["upload", "download"]:
        raise ValueError(f"Invalid operation: {operation}. Must be 'upload' or 'download'.")

    config = utils.load_config(config_path)

    if file_type not in config:
        raise ValueError(f"Invalid file type: {file_type}. Must be one of: {', '.join(config.keys())}")

    file_paths = config[file_type]

    logger.info(f"Starting {operation} operation for bucket: {bucket_name}")
    for file_path in file_paths:
        if operation == "upload":
            upload_to_s3(
                file_name=file_path,
                bucket_name=bucket_name,
                s3_key=file_path
            )
        elif operation == "download":
            download_from_s3(
                file_name=file_path,
                bucket_name=bucket_name,
                s3_key=file_path
            )

    logger.info(f"{operation.capitalize()} operation completed successfully for bucket: {bucket_name}")


def sync_raw_playlists_with_s3(bucket_name, operation, config_path="config/config.yaml"):
    """
    Synchronize raw playlist files with S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        operation (str): The operation to perform ("upload" or "download").
        config_path (str): Path to the configuration file (default: "config/config.yaml").
    """
    if operation not in ["upload", "download"]:
        raise ValueError(f"Invalid operation: {operation}. Must be 'upload' or 'download'.")

    logger.info(f"Loading configuration from: {config_path}")
    config = utils.load_config(config_path)

    playlist_files = []
    for playlist_name in config["playlists"].keys():
        file_name = f"data/raw/playlists/{slugify(playlist_name, separator='_')}.json"
        playlist_files.append({
            "file_name": file_name,
            "s3_key": file_name
        })

    logger.info(f"Starting {operation} operation for bucket: {bucket_name}")

    for file in playlist_files:
        if operation == "upload":
            upload_to_s3(
                file_name=file["file_name"],
                bucket_name=bucket_name,
                s3_key=file["s3_key"]
            )
        elif operation == "download":
            download_from_s3(
                file_name=file["file_name"],
                bucket_name=bucket_name,
                s3_key=file["s3_key"]
            )

    logger.info(f"{operation.capitalize()} operation completed successfully for bucket: {bucket_name}")
