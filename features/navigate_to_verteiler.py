# File: features/navigate_to_verteiler.py

import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def sniff_jsessionid_from_cdp(driver: WebDriver, timeout: int = 15):
    """
    Uses Chrome DevTools Protocol (CDP) logs to find the Verteiler jsessionid URL.
    """
    print("🔍 Listening to Chrome DevTools logs for Verteiler link...")
    time.sleep(timeout)  # Wait for internal network activity to complete

    try:
        logs = driver.get_log("performance")
        for entry in logs:
            message = json.loads(entry["message"])
            url = message.get("message", {}).get("params", {}).get("request", {}).get("url", "")

            if "distributionLists;jsessionid=" in url:
                print("✅ Verteiler URL with jsessionid detected:")
                print(url)
                return url

        print("❌ No Verteiler jsessionid link found in DevTools logs.")
    except Exception as e:
        print(f"⚠️ Error while sniffing CDP logs: {e}")

    return None
