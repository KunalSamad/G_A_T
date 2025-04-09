# File name suggestion: browser_launcher.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

# Set path to your ChromeDriver
CHROMEDRIVER_PATH = "C:\\Windows\\chromedriver.exe"

def create_browser():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start maximized
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

if __name__ == "__main__":
    driver = create_browser()
    driver.get("https://www.gmx.net")
    print("Browser is open. Close it manually using the 'X' button in the top right corner.")

    try:
        while True:
            time.sleep(1)
            # If the browser is closed manually, break the loop
            if not driver.service.is_connectable():
                break
    except KeyboardInterrupt:
        pass
    finally:
        try:
            driver.quit()
        except:
            pass
