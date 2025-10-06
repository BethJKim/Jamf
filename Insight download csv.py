import os, time
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser

download_dir = r"C:\Users\bkim\Downloads"

def wait_for_download(download_dir, timeout=50):
    end_time = time.time() + timeout
    before = set(os.listdir(download_dir))
    while time.time() < end_time:
        after = set(os.listdir(download_dir))
        new_files = after - before
        for f in new_files:
            if not f.endswith(".crdownload"):
                return os.path.join(download_dir, f)
        time.sleep(1)
    raise TimeoutError (f"file has not been downloaded in {timeout} seconds")


config = ConfigParser()
config.read("config.ini")
username = config["jira"]["username"]
password = config["jira"]["password"]
# Start Chrome automatically with matching driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# login to Jira
driver.get("https://jira.sd62.bc.ca/login.jsp")
id_input= WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="login-form-username"]'))
)
id_input.send_keys(username)
time.sleep(2)
pw_input = driver.find_element(By.XPATH, '//*[@id="login-form-password"]')
pw_input.send_keys(password)
pw_input.send_keys(Keys.ENTER)
time.sleep(5)

#Navigate to Insight
driver.get("https://jira.sd62.bc.ca/secure/ObjectSchema.jspa?id=6&typeId=108&view=list&objectId=67616")
time.sleep(5)
print("Opened:", driver.title)

#download CVS file
bulk_actions_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="rlabs-actions-object-tools-button"]/span'))
)
bulk_actions_btn.click()
export_objects_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="rlabs-actions-object-tools"]'))
)
export_objects_btn.click()
export_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="rlabs-insight-dialog"]/div/div[2]/button'))
)
export_btn.click()
download_file = wait_for_download(download_dir)
print ("Download complete", download_file)

#get serial numbers of recycled devices from csv file
serial_number = []
valid_status = {"Recycled - Damaged", "Recycled - End of Life"}

with open(download_file, newline="", encoding="utf-8") as f:
    reader = list(csv.DictReader(f))
    for row in reader:
        print(row)
        status = row.get("Disposition Status", "").strip()
        if status in valid_status:
            serial_number.append(row.get("Serial Number", "").strip())

if serial_number:
    print(f"found {len(serial_number)} as recycled devices:")
    for sn in serial_number:
        print("- ", sn)
else:
    print("No serial number to be found")

#login to Jamf
jamf_url = "https://casper.sd62.bc.ca:8443/"
jamf_user = config["jamf"]["username"]
jamf_pass = config["jamf"]["password"]

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(jamf_url)

username_input = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.input[type='text'][data-wa='nebula--form-element']"))
)
username_input.send_keys(jamf_user)

password_input = driver.find_element(By.CSS_SELECTOR, "input.input[type='password'][data-wa='nebula--form-element']")
password_input.send_keys(jamf_pass)
password_input.send_keys(Keys.ENTER)
time.sleep(10)

#go to Devices> Search Inventory

devices_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Devices"))
)
devices_btn.click()

driver.execute_script("""
function clickSearchInventory() {
    const shell = document.querySelector('jamf-app-shell');
    if (!shell) return false; // not ready yet
    const items = shell.shadowRoot.querySelectorAll('div[data-test-id="single-item"]');
    for (const item of items) {
        if (item.textContent.includes('Search Inventory')) {
            item.click();
            return true;
        }
    }
    return false;
}

setTimeout(() => {
    clickSearchInventory();
}. 5000)
""")

#Search and update the device status
updated_serials= []
not_found_serials = []
for row in reader:
        serial_number.append(row.get("Serial Number", "").strip())
time.sleep(10)

for sn in serial_number:
    search_input = driver.execute_script("""
            const shell = document.querySelector('jamf-app-shell');
            return shell ? shell.shadowRoot.querySelector('input#query') : null;
        """)

    if search_input:
        search_input.clear()
        search_input.send_keys(sn)
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            # Adjust this selector based on the element that shows search results
            result_element = driver.execute_script("""
                        const shell = document.querySelector('jamf-app-shell');
                        const root = shell.shadowRoot;
                        return root.querySelector('jamf-inventory-table tbody tr');
                    """)
            if result_element:
                updated_serials.append(sn)
            else:
                not_found_serials.append(sn)
        except:
            not_found_serials.append(sn)

    else:
        print(f"{sn} does not exist in the inventory")
        not_found_serials.append(sn)
#print the result

print(f"\nTotal updated devices: {len(updated_serials)}")
for sn in updated_serials:
    print("-",sn)
print(f"\nTotal not found in Jamf: {len(not_found_serials)}")
for sn in updated_serials:
    print("-", sn)