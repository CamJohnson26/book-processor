import os
from os.path import join

import boto3
from botocore.exceptions import NoCredentialsError
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


def upload_files():
    files = get_input_files()

    for file in files:
        file_name = file.split("/")[-1]
        object_name = join('unprocessed', file_name)

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
