import os, time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

download_dir = r"C:\Users\bkim\Downloads"

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
    const root = shell.shadowRoot;
    const items = root.querySelectorAll('div[data-test-id="single-item"]');
    for (const item of items) {
        if (item.textContent.includes('Search Inventory')) {
            item.click();
            return true;
        }
    }
    return false;
}

let clicked = false;
let attempts = 0;
const interval = setInterval(() => {
    if (clickSearchInventory() || attempts > 20) clearInterval(interval);
    attempts++;
}, 500);
""")

#Search and update the device status

for row in reader:
        serial_number.append(row.get("Serial Number", "").strip())

for sn in serial_number:
    search_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "query"))
    )
    search_input.clear()
    search_input.send_keys(sn)
    search_input.send_keys(Keys.ENTER)
    time.sleep(5)

    updated_serials.append(sn)

#print the result

print(f"\nTotal updated devices: {len(updated_serials)}")
print("Updated serial numbers:")
for sn in updated_serials:
    print("-", sn)