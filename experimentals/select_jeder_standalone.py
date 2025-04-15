import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver

# Config
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHROMEDRIVER_PATH = "C:\\Windows\\chromedriver.exe"
USER_DATA_DIR = "C:\\Temp\\GMX_Profile"

def launch_chrome_debugger():
    print("🚀 Launching Chrome in debugging mode...")
    subprocess.Popen([
        CHROME_PATH,
        "--remote-debugging-port=9222",
        f"--user-data-dir={USER_DATA_DIR}"
    ])
    time.sleep(3)

def connect_debug_chrome() -> WebDriver:
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def select_jeder_option(driver: WebDriver):
    def recursive_select(driver, level=0):
        indent = "  " * level
        try:
            select_element = driver.find_element(By.CSS_SELECTOR, 'select[name="fieldset:modeDropDown"]')
            dropdown = Select(select_element)
            dropdown.select_by_value("2")  # "2" corresponds to "Jeder (öffentlich)"
            print(f"{indent}✅ Selected 'Jeder (öffentlich)' from dropdown at level {level}")
            return True
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {i} at level {level}")
                if recursive_select(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return False

    print("🔽 Searching for dropdown to select 'Jeder (öffentlich)'...")
    if not recursive_select(driver):
        print("❌ Dropdown not found or could not select value.")

if __name__ == "__main__":
    launch_chrome_debugger()
    driver = connect_debug_chrome()
    print(f"✅ Connected to Chrome | Current URL: {driver.current_url}")
    driver.get("https://www.gmx.net")

    input("📌 Navigate to Verteiler creation form and press Enter to continue...")
    select_jeder_option(driver)
