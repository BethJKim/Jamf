import requests
from requests.auth import HTTPBasicAuth

#Login to Jira
id= "bkim"
pw = "Wltjslchlrh12!"
jira_url = "https://jira.sd62.bc.ca/login.jsp?os_destination=%2Fprojects%2FSD62IT%2Freports%2Fworkload&permissionViolation=true"

url = f"{jira_url}"
response = requests.get(
    url,
    auth=HTTPBasicAuth(id, pw),
)