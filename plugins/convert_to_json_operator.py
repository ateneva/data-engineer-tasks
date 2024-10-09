from typing import Sequence
import logging
import os
import csv
import json
import tempfile
import uuid

from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.models import BaseOperator
from helpers.csv_handling import CSVHandler


class ConvertToJSON(BaseOperator):
    template_fields: Sequence[str] = ("source_gcs_prefix")

    def __init__(
            self,
            gcp_conn_id: str,
            source_gcs_bucket: str,
            source_gcs_prefix: str,
            target_gcs_bucket: str,
            target_gcs_prefix: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.source_gcs_bucket = source_gcs_bucket
        self.source_gcs_prefix = source_gcs_prefix
        self.target_gcs_bucket = target_gcs_bucket
        self.target_gcs_prefix = target_gcs_prefix

    def download_files_from_gcs(self):
        """
        Downloads a file from GCS using GCSHook
        :return: temp folder where the downloaded file is stored
        """
        gcs = GCSHook(gcp_conn_id=self.gcp_conn_id)
        blobs = gcs.list(self.source_gcs_bucket, prefix=self.source_gcs_prefix, delimiter='/')
        print(f'available files: {blobs}')

        # download all identified files in temp directory
        downloads = []
        temp_folder = tempfile.mkdtemp()
        for file in blobs:
            file_object = self.source_gcs_prefix + file
            file_full_path = os.path.join(temp_folder, file)
            downloaded_file = gcs.download(self.gcs_bucket, file_object, file_full_path)
            downloads.append(downloaded_file)
            logging.info(f"{downloads} files downloaded in {file_full_path}")
        return temp_folder

    def write_to_gcs_file(self, temp_folder, file_name):
        """
            Uploads new line delimited json to GCS using GCSHook
        """

        unique_file_name = f'{file_name}_{uuid.uuid4()}.json'
        temp_file_name = f'{temp_folder}/{unique_file_name}'

        logging.info(f"Uploading {temp_file_name} to GCS to {self.target_gcs_bucket}/{self.target_gcs_prefix}")
        hook = GCSHook(gcp_conn_id=self.gcp_conn_id)
        hook.upload(
            bucket_name=self.target_gcs_bucket,
            object_name=f"{self.target_gcs_prefix}/{unique_file_name}",
            filename=os.path.abspath(temp_file_name)
        )

    def execute(self, context):
        """
            Downloads a CSV file, converts it to JSON new line delimited and uploads it to GCS
        """
        pass
