"""This module converts text to csv"""
import csv

def text2csv(text):
    """This is a converter for TEXT to CSV

    :param text string
    """
    with open("text2csv.csv", "w") as file:
      writer = csv.writer(file)
      writer.writerow(text)
