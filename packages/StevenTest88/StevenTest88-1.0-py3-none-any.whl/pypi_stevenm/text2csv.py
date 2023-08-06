import csv

def text2csv(text):
    with open("text2csv.csv", "w") as file:
      writer = csv.writer(file)
      writer.writerow(text)
