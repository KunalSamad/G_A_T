# File: experimentals/test_click_verteiler_button.py

import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import socket

DEBUGGER_PORT = 9222
USER_DATA_DIR = "C:\\Temp\\GMX_Profile"
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("localhost", port)) == 0

def launch_chrome_with_debugging():
    print("🚀 Launching Chrome with remote debugging...")
    subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={DEBUGGER_PORT}",
        f"--user-data-dir={USER_DATA_DIR}"
    ])
    time.sleep(3)  # Give it a moment to launch

def connect_to_chrome():
    if not is_port_open(DEBUGGER_PORT):
        launch_chrome_with_debugging()

    print("✅ Connecting to running Chrome session...")
    options = Options()
    options.debugger_address = f"127.0.0.1:{DEBUGGER_PORT}"
    driver = webdriver.Chrome(options=options)
    return driver

def find_and_click_button_recursively(driver, level=0):
    indent = "  " * level
    try:
        button = driver.find_element(By.CSS_SELECTOR, 'button[data-webdriver="createDistributionListButton"]')
        button.click()
        print(f"{indent}✅ Clicked 'Neuen Verteiler anlegen' button at iframe level {level}")
        return True
    except:
        pass

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"{indent}🔍 Found {len(iframes)} iframe(s) at level {level}")
    for index, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            print(f"{indent}➡️ Entering iframe {index} at level {level}")
            if find_and_click_button_recursively(driver, level + 1):
                return True
            driver.switch_to.parent_frame()
        except:
            driver.switch_to.parent_frame()

    return False

if __name__ == "__main__":
    driver = connect_to_chrome()
    print(f"🌐 Current URL: {driver.current_url}")
    input("📌 Please navigate to the Verteiler page and press Enter to begin...\n")

    print("⏳ Starting recursive iframe search for the Verteiler create button...")
    success = find_and_click_button_recursively(driver)

    if not success:
        print("❌ Button not found. Make sure you're on the Verteiler page.")
