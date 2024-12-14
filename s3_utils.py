import os
from os.path import join

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

from file_utils import get_input_files

load_dotenv()

# Define your S3 configuration
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
REGION = os.environ.get("REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION,
    endpoint_url=S3_ENDPOINT,
)

bucket_folder = 'unprocessed'


def upload_files():
    files = get_input_files()

    for file in files:
        file_name = file.split("/")[-1]
        object_name = join(bucket_folder, file_name)

        try:
            # Upload the file
            s3_client.upload_file(file, BUCKET_NAME, object_name)
            print(f"File uploaded successfully to s3://{BUCKET_NAME}/{object_name}")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
        except Exception as e:
            print(f"An error occurred: {e}")


def get_first_file_in_folder(folder_name=bucket_folder):
    """
    Get the first file in a specific folder in an S3 bucket.

    :return: The key (path) of the first file found, or None if the folder is empty
    """
    try:
        # List objects with the folder prefix
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_name)

        if 'Contents' in response:
            # Return the key of the first file (skipping the folder itself if it's listed)
            for obj in response['Contents']:
                if obj['Key'] != folder_name:  # Avoid returning the folder itself
                    return obj['Key']
        return None  # Folder is empty or doesn't exist

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def download_all_files_in_folder(folder_name=bucket_folder, local_folder='processing'):
    """
    Download all files from a specific folder in an S3 bucket to a local directory.

    :return: List of downloaded file paths
    """
    downloaded_files = []

    try:

        # List objects with the folder prefix
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_name)

        if 'Contents' not in response:
            print(f"No files found in folder: {folder_name}")
            return downloaded_files

        # Ensure local folder exists
        os.makedirs(local_folder, exist_ok=True)

        # Download each file
        for obj in response['Contents']:
            file_key = obj['Key']

            # Skip if the object is the folder itself
            if file_key.endswith('/') and file_key == folder_name:
                continue

            # Define local file path
            local_file_path = os.path.join(local_folder, os.path.basename(file_key))

            # Download the file
            s3_client.download_file(BUCKET_NAME, file_key, local_file_path)
            downloaded_files.append(local_file_path)
            print(f"Downloaded: {file_key} to {local_file_path}")

        return downloaded_files

    except NoCredentialsError:
        print("AWS credentials not available.")
        return []
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def delete_file_in_folder(file_name):
    """
    Delete a specific file from a folder in an S3 bucket.

    :param file_name: Name of the file to delete in the S3 bucket
    :return: True if the file was deleted, False otherwise
    """
    file_key = join(bucket_folder, file_name)

    try:
        # Delete the file
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)
        print(f"Deleted file: {file_key}")
        return True
    except Exception as e:
        print(f"An error occurred while deleting file '{file_key}': {e}")
        return False