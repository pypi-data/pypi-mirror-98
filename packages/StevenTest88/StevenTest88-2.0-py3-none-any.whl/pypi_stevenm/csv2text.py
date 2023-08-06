"""This module converts CSV files to text"""

import csv

class Converter:
    """A simple converter for CSV to Text"""
    def csv2text(self, file):
        """
        Convert CSV to Text
        :param file: CSV file
        :return: string
        """
        with open(file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

Converter.csv2text("text2csv.csv")
