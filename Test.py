# Open browser
# selenium 4
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
time.sleep(5)

# Go to webpage
driver.get("https://www.google.com")
time.sleep(2)
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Python Selenium")
search_box.send_keys(Keys.ENTER)
time.sleep(5)
print("Page title:", driver.title)

