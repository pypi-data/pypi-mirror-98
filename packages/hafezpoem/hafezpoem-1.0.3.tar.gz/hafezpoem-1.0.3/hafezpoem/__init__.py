import csv
import random
import pkg_resources
from importlib.resources import open_text
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

def get_random_fal():
    with open('data/poems.csv', mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        rnd = random.randrange(0, 495)
        for row in csv_reader:
            if rnd == line_count:
                return row["poem"]
            line_count += 1
