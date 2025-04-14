# File: features/navigate_to_verteiler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

def extract_verteiler_href(driver: WebDriver):
    print("🔍 Looking for Verteiler link inside iframes...")

    time.sleep(2)  # Small delay to allow page elements to render
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"📦 Found {len(iframes)} iframe(s). Scanning each...")

    for index, iframe in enumerate(iframes):
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe)
            print(f"➡️ Switched to iframe {index}...")

            # Look for the Verteiler link
            verteiler = driver.find_element(By.CSS_SELECTOR, 'a[data-webdriver="MAILINGLISTS"]')
            href = verteiler.get_attribute("href")
            if href:
                print("✅ Found Verteiler link with jsessionid:")
                print(href)
                return href
        except:
            continue

    driver.switch_to.default_content()
    print("❌ Verteiler link not found in any iframe.")
    return None
