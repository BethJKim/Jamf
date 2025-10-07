import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
import csv

config = ConfigParser()
config.read("config.ini")



with open(csv_file, newline='', encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if "Recycled" in