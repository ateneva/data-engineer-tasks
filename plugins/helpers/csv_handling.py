
"""Library to Tackle the most frequently CSV conversions"""

import csv
import json
import tempfile
import logging
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

    def change_csv_delimiters(self, output_file, new_delimiter):
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

    def csv_to_pretty_json(self, json_file_path):
        """
        converts a CSV file to pretty json
            :param json_file_path: file path where the json file should be saved
        """
        data = []
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            for row in csv_reader:
                data.append(row)

        with open(json_file_path, 'w', encoding='UTF-8') as json_file:
            json.dump(data, json_file, indent=4)

    def csv_to_new_line_delimited_json(self, json_file_path):
        """
        converts a CSV file to new json delimited json
            :param json_file_path: file path where the json file should be saved
        """
        data = []
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            for row in csv_reader:
                data.append(row)

        with open(json_file_path, 'w', encoding='UTF-8') as json_file:
            for record in data:
                if len(record) > 0:
                    json_file.write(json.dumps(record) + '\n')

    def convert_zipped_csv_to_new_line_delimited_json(self, file_delimiter, json_local_path):
        """converts zipped csv files to json new line delimited"""
        json_data = []
        with ZipFile(self.file_path) as myzip:
            for file in myzip.namelist():
                if file.endswith('.csv'):
                    with myzip.open(file) as f:
                        with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=True):
                            data = f.read().decode('utf-8', 'ignore').splitlines()
                            csv_reader = csv.DictReader(data, delimiter=file_delimiter)
                            logging.info('Constructing a Dictionary started')
                            for row in csv_reader:
                                json_data.append(row)
                else:
                    raise OSError

        logging.info('Conversion to new line delimited json started')
        with open(json_local_path, 'w', encoding='utf-8') as json_file:
            for record in json_data:
                if len(record) > 0:
                    json_file.write(json.dumps(record) + '\n')


# Example usage:
file_specs = CSVHandler('/Users/angelina.teneva/Downloads/gcp_datasets_Outbrain Kaggle Competition_page_views_sample.csv.zip', 'UTF-8', ',')
file_specs.convert_zipped_csv_to_new_line_delimited_json(
    ',',
    '/Users/angelina.teneva/Documents/outbrain_kaggle.json'
)
