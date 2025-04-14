# File: test_find_verteiler_link.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def connect_to_existing_chrome():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    return driver

def find_verteiler_link(driver):
    try:
        time.sleep(2)
        print("🔎 Checking for iframes...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"📦 Found {len(iframes)} iframe(s).")

        # Try each iframe until Verteiler link is found
        for idx, iframe in enumerate(iframes):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)
                print(f"➡️  Switched to iframe {idx}...")

                # Try to find the Verteiler link
                verteiler = driver.find_element(By.CSS_SELECTOR, 'a[data-webdriver="MAILINGLISTS"]')
                href = verteiler.get_attribute("href")
                if href:
                    print("✅ Found Verteiler link with jsessionid:")
                    print(href)
                    return href
            except:
                continue  # try next iframe

        # Fallback: Try without iframe
        driver.switch_to.default_content()
        print("🔁 Trying to find Verteiler link without switching to iframe...")
        verteiler = driver.find_element(By.CSS_SELECTOR, 'a[data-webdriver="MAILINGLISTS"]')
        href = verteiler.get_attribute("href")
        if href:
            print("✅ Found Verteiler link outside iframe:")
            print(href)
            return href

        print("❌ Verteiler link not found.")

    except Exception as e:
        print(f"❌ Error while searching for Verteiler: {e}")
    return None


if __name__ == "__main__":
    try:
        driver = connect_to_existing_chrome()
        print("✅ Connected to Chrome.")
        print("🌐 Current URL:", driver.current_url)
    except Exception as e:
        print("❌ Failed to connect to Chrome.")
        print("Error:", str(e))
        exit()

    input("📌 Make sure you're on the Settings page with Verteiler visible, then press Enter...\n")
    find_verteiler_link(driver)
