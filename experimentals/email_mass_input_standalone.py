# File: experimentals/email_mass_input_standalone.py

import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

# 🔧 CONFIGURATIONS
CHROMEDRIVER_PATH = "C:\\Windows\\chromedriver.exe"
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
USER_DATA_DIR = "C:\\Temp\\GMX_Profile"
EMAILS_FILE_PATH = "Output/data_ids.txt"

def launch_chrome_debugger():
    print("🚀 Launching Chrome in debugging mode...")
    subprocess.Popen([
        CHROME_PATH,
        "--remote-debugging-port=9222",
        f"--user-data-dir={USER_DATA_DIR}"
    ])
    print("⌛ Waiting 3 seconds for Chrome to start...")
    time.sleep(3)

def launch_debug_chrome() -> WebDriver:
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def load_emails_from_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def insert_all_emails_at_once(driver: WebDriver, email_list: list[str]):
    print("📩 Attempting to insert all emails at once...")

    def search_and_insert(driver, level=0):
        indent = "  " * level
        try:
            input_field = driver.find_element(By.CSS_SELECTOR, "input.select2-input")
            all_emails = ", ".join(email_list)
            input_field.send_keys(all_emails)
            print(f"{indent}✅ Inserted {len(email_list)} emails at once.")
            return True
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {i} at level {level}")
                if search_and_insert(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()
        return False

    if not search_and_insert(driver):
        print("❌ Could not locate or insert into email input field.")

if __name__ == "__main__":
    launch_chrome_debugger()
    driver = launch_debug_chrome()

    print(f"✅ Connected to Chrome | Current URL: {driver.current_url}")
    driver.get("https://www.gmx.net")

    input("📌 Manually navigate to Verteiler creation form and press Enter to insert all emails...")

    emails = load_emails_from_file(EMAILS_FILE_PATH)
    insert_all_emails_at_once(driver, emails)
