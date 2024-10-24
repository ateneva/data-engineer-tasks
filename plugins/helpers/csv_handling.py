
"""Library to Tackle the most frequently CSV conversions"""

import csv
import json
import gzip
import logging
import time
from datetime import datetime
from zipfile import ZipFile
from dataclasses import dataclass

logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)


@dataclass
class CSVHandler:
    """
    Module to handle the most frequent csv file manipulations:
        file_path: the path where the original file is located
        csv_encoding: the encoding of the original csv file
        csv_delimiter: the delimiter of the original csv file
    """
    file_path: str
    csv_encoding: str
    csv_delimiter: str

    def change_csv_delimiters(self, output_file: str, new_delimiter: str):
        """
        reads a CSV file and writes its content to a new CSV with the wanted delimiter
            :param output_file: full path where the updated file should be saved
            :param new_delimiter: delimiter with which the updated file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
            with open(output_file, 'w', newline='', encoding="utf8") as output_csv_file:
                writer = csv.DictWriter(output_csv_file, reader.fieldnames, delimiter=new_delimiter)
                writer.writeheader()
                writer.writerows(reader)
        logging.info(f"Converting {self.file_path} to {output_file} complete")

    def csv_to_gzip(self, gzip_file_path: str):
        """
        converts a CSV file to pretty json
            :param gzip_file_path: file path where the json file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            data = csv_file.read()
            with gzip.open(gzip_file_path, 'wb') as f:
                f.write(str.encode(data))

    def csv_to_pretty_json(self, json_file_path: str):
        """
        converts a CSV file to pretty json
            :param json_file_path: file path where the json file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            data = [row for row in csv_reader]

            with open(json_file_path, 'w', encoding='UTF-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

    def csv_to_new_line_delimited_json(self, json_file_path: str):
        """
        converts a CSV file to new json delimited json
            :param json_file_path: file path where the json file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            data = [row for row in csv_reader]

            with open(json_file_path, 'w', encoding='UTF-8') as json_file:
                for record in data:
                    record.update({"_processed_at": f"{datetime.now()}"})
                    if len(record) > 0:
                        json_file.write(json.dumps(record, ensure_ascii=False) + '\n')

    def zipped_csv_to_new_line_delimited_json(self, json_file_path: str, compressed=True):
        """converts zipped csv files to (compressed) json new line delimited
            :param json_file_path: file path where the json file should be saved
            :param compressed: if the converted file should be gzip compressed or not
        """
        with ZipFile(self.file_path) as myzip:
            for file in myzip.namelist():
                if file.endswith('.csv'):
                    with myzip.open(file) as f:
                        data = f.read().decode(self.csv_encoding, 'ignore').splitlines()
                        csv_reader = csv.DictReader(data, delimiter=self.csv_delimiter)
                        print('Started constructing a dictionary object')
                        json_data = [row for row in csv_reader]

                        print('Started converting to new line delimited json')
                        if compressed:
                            with gzip.open(json_file_path + '.gz', 'wb') as json_file:
                                for record in json_data:
                                    record.update({"_processed_at": f"{datetime.now()}"})
                                    record_str = json.dumps(record, ensure_ascii=False)
                                    if len(record) > 0:
                                        json_file.write(str.encode(record_str + '\n'))
                        else:
                            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                                for record in json_data:
                                    record.update({"_processed_at": f"{datetime.now()}"})
                                    if len(record) > 0:
                                        json_file.write(json.dumps(record, ensure_ascii=False) + '\n')
                        print(f'Converted file is {json_file_path}')
                else:
                    raise OSError

# Example usage:

data_engineer_jobs = CSVHandler('/Users/angelina.teneva/Documents/DataEngineer.csv', 'UTF-8', ',')
data_engineer_jobs.csv_to_gzip(
     '/Users/angelina.teneva/Documents/data_engineer_jobs.csv.gz'
 )

data_engineer_jobs.csv_to_pretty_json(
      '/Users/angelina.teneva/Documents/data_engineer_jobs.json'
  )

data_engineer_jobs.csv_to_new_line_delimited_json(
      '/Users/angelina.teneva/Documents/data_engineer_jobs_new_line_delimited.json'
  )

outbrain = CSVHandler(
    '/Users/angelina.teneva/Downloads/gcp_datasets_Outbrain Kaggle Competition_page_views_sample.csv.zip',
    'UTF-8', ',')
outbrain.zipped_csv_to_new_line_delimited_json(
     '/Users/angelina.teneva/Documents/outbrain_comprehension_kaggle.json',
     compressed=True
)

netflix = CSVHandler(
    '/Users/angelina.teneva/Downloads/gcp_datasets_zipped_1000-netflix-shows.zip', 'UTF-8', ',')
netflix.zipped_csv_to_new_line_delimited_json(
     '/Users/angelina.teneva/Documents/netflix_shows.json',
     compressed=False
)