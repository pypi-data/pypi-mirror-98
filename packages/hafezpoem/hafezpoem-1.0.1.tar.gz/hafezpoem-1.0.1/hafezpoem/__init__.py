import csv
import random


def get_random_fal():
    with open('poems.csv', mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        rnd = random.randrange(0, 495)
        for row in csv_reader:
            if rnd == line_count:
                return row["poem"]
            line_count += 1
