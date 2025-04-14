import subprocess
import time
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
    time.sleep(3)

def connect_to_chrome():
    if not is_port_open(DEBUGGER_PORT):
        launch_chrome_with_debugging()

    print("✅ Connecting to running Chrome session...")
    options = Options()
    options.debugger_address = f"127.0.0.1:{DEBUGGER_PORT}"
    driver = webdriver.Chrome(options=options)
    return driver

def recursive_iframe_fill(driver, kun_number, level=0):
    indent = "  " * level
    try:
        input_box = driver.find_element(By.CSS_SELECTOR, 'input[data-webdriver="name"]')
        input_box.clear()
        input_box.send_keys(f"kun{kun_number}")
        print(f"{indent}✅ Filled Verteiler name with 'kun{kun_number}' at iframe level {level}")
        return True
    except:
        pass

    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for idx, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            print(f"{indent}➡️ Entering iframe {idx} at level {level}")
            if recursive_iframe_fill(driver, kun_number, level + 1):
                return True
            driver.switch_to.parent_frame()
        except:
            driver.switch_to.parent_frame()
    return False

if __name__ == "__main__":
    driver = connect_to_chrome()
    print(f"🌐 Current URL: {driver.current_url}")
    input("📌 Navigate to the Verteiler creation form and press Enter...\n")

    print("🔍 Searching recursively for Verteiler name field...")
    success = recursive_iframe_fill(driver, kun_number=1)

    if not success:
        print("❌ Could not find or fill the Verteiler name field.")
