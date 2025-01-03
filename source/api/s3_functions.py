import os
import boto3
from logs.logger_config import logger
from source.api import secrets_functions


aws_secrets = secrets_functions.get_secrets('aws')

# Create S3 resource
s3 = boto3.resource(
   service_name='s3',
   region_name='eu-central-1',
   aws_access_key_id=aws_secrets.get('aws_access_key_id'),
   aws_secret_access_key=aws_secrets.get('aws_secret_access_key'),
)


def upload_to_s3(file_name, bucket_name, s3_key):
    try:
        s3.Bucket(bucket_name).upload_file(Filename=file_name, Key=s3_key)
        logger.info(f"'{file_name}' has been uploaded to bucket '{bucket_name}' as '{s3_key}'.")
    except Exception as e:
        logger.error(f"Error uploading file: {e}")


def upload_files_to_s3(bucket_name, files):
    for file in files:
        upload_to_s3(
            file_name=file['file_name'],
            bucket_name=bucket_name,
            s3_key=file['s3_key']
        )


def download_from_s3(file_name, bucket_name, s3_key):
    directory = os.path.dirname(file_name)
    os.makedirs(directory, exist_ok=True)
    try:
        s3.Bucket(bucket_name).download_file(Key=s3_key, Filename=file_name)
        logger.info(f"File '{s3_key}' has been downloaded from bucket '{bucket_name}' to local path '{file_name}'.")
    except Exception as e:
        logger.error(f"Error downloading file: {e}")