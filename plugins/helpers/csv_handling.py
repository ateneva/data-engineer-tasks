
"""Library to Tackle the most frequently CSV conversions"""

import csv
import json
from dataclasses import dataclass


@dataclass
class CSVHandler:
    """
    Module to handle the most frequent csv file manipulations:
        csv_file_path: the path where the original csv is located
        csv_encoding: the encoding of the original csv file
        csv_delimiter: the delimiter of the original csv file
    """
    csv_file_path: str
    csv_encoding: str
    csv_delimiter: str

    def change_csv_delimiters(self, output_file, new_delimiter):
        """
        reads a CSV file and writes its content to a new CSV with the wanted delimiter
            :param output_file: full path where the updated file should be saved
            :param new_delimiter: delimiter with which the updated file should be saved
        """
        with open(self.csv_file_path, 'r', encoding=self.csv_encoding) as csv_file:
            with open(output_file, 'w', newline='', encoding="utf8") as output_csv_file:
                reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
                writer = csv.DictWriter(output_csv_file, reader.fieldnames, delimiter=new_delimiter)
                writer.writeheader()
                writer.writerows(reader)
        print(f"Converting {self.csv_file_path} to {output_file} complete")

    def csv_to_pretty_json(self, json_file_path):
        """
        converts a CSV file to pretty json file
            :param json_file_path: file path where the json file should be saved
        """
        data = []
        with open(self.csv_file_path, 'r', encoding=self.csv_encoding) as csv_file:
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
        with open(self.csv_file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            for row in csv_reader:
                data.append(row)

        with open(json_file_path, 'w', encoding='UTF-8') as json_file:
            for record in data:
                if len(record) > 0:
                    json_file.write(json.dumps(record) + '\n')


# Example usage:
file_specs = CSVHandler('/Users/angelina.teneva/Documents/data_engineer.csv', 'UTF-8', ',')
file_specs.change_csv_delimiters(
    '/Users/angelina.teneva/Documents/data_engineer_tabbed.csv',
    '|'
)
