import boto3
import os
from logs.logger_config import logger


# Create S3 resource
s3 = None


def upload_to_s3(file_name, bucket_name, s3_key):
    try:
        s3.Bucket(bucket_name).upload_file(Filename=file_name, Key=s3_key)
        logger.info(f"'{file_name}' has been uploaded to bucket '{bucket_name}' as '{s3_key}'.")
    except Exception as e:
        logger.error(f"Error uploading file: {e}")


def download_from_s3(file_name, bucket_name, s3_key):
    directory = os.path.dirname(file_name)
    os.makedirs(directory, exist_ok=True)
    try:
        s3.Bucket(bucket_name).download_file(Key=s3_key, Filename=file_name)
        logger.info(f"File '{s3_key}' has been downloaded from bucket '{bucket_name}' to local path '{file_name}'.")
    except Exception as e:
        logger.error(f"Error downloading file: {e}")


# download_from_s3(file_name=file_name, bucket_name=bucket_name, s3_key=s3_key)


# # Access the bucket
# bucket = s3.Bucket(bucket_name)
#
# # Print all files and folders
# logger.info(f"Files and folders in the bucket '{bucket_name}':")
# for obj in bucket.objects.all():
#     logger.info(obj.key)
