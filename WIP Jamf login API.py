from configparser import ConfigParser
import requests


config = ConfigParser()
config.read("config.ini")

jamf = config[jamf]
jamf_user = jamf["user"]
jamf_pass = jamf["password"]

auth_res = requests.post(
    f"{jamf_url}/api/v1/auth/token",
    auth=(jamf_user, jamf_pass),
)

if

