import csv


def csv2text(file):
    with open(file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

csv2text("text2csv.csv")
