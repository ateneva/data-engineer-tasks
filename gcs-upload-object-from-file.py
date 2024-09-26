import os
import logging
from google.cloud import storage
from datetime import datetime

KEY_PATH = "/Users/angelina.teneva/Documents/data-geeking-gcp-c710229c3108.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

LOCAL_PATH = '/Users/angelina.teneva/Downloads/'
file_names = ['data_engineer.csv', 'usa_median_household_income.csv']


def upload_blob(bucket_name, gcs_prefix, source_file_name, destination_blob_name):
    """Uploads a file to specific GCS bucket.

    Args:
        bucket_name = "your-bucket-name
        gcs_prefix = "/sub-folder within bucket"
        source_file_name = "local/path/to/file"
        destination_blob_name = "storage-object-name"
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_prefix + '/' + destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logging.info(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


if __name__ == '__main__':
    for file in file_names:
        upload_blob(
            'eu-data-challenge',
            file.split('.')[0] + '/' + datetime.now().strftime('%Y%m%d'),
            LOCAL_PATH + file,
            datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file
        )