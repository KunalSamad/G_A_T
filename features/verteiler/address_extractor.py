# File: features/verteiler/address_extractor.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

def extract_verteiler_email_address(driver: WebDriver, delay: float = 2.0) -> str:
    """
    Recursively searches all iframes to extract the generated Verteiler email address
    shown under 'Name des Verteilers:' (e.g. kun1%annettdiga@gmx.net).

    Returns the email address as string if found, else returns an empty string.
    """
    def _recursive_search(driver, level=0):
        indent = "  " * level
        try:
            para = driver.find_element(By.CSS_SELECTOR, 'p[data-webdriver="completeAddressParagraph"]')
            email = para.find_element(By.TAG_NAME, 'strong').text.strip()
            print(f"{indent}✅ Found Verteiler email: {email} at iframe level {level}")
            return email
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for idx, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {idx} at level {level}")
                result = _recursive_search(driver, level + 1)
                if result:
                    return result
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return ""

    print("🔍 Searching recursively for Verteiler email address...")
    time.sleep(delay)  # Let the page render
    email = _recursive_search(driver)
    if not email:
        print("❌ Verteiler email address not found.")
    return email
