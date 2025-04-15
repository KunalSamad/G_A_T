# File: features/verteiler/save_button_clicker.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

def click_speichern_button(driver: WebDriver) -> bool:
    """
    Recursively searches all iframes and clicks the 'Speichern' button for Verteiler creation.
    Returns True if successful, False otherwise.
    """
    def _recursive_click(driver, level=0):
        indent = "  " * level
        try:
            speichern_button = driver.find_element(By.CSS_SELECTOR, 'button[data-webdriver="save"]')
            speichern_button.click()
            print(f"{indent}✅ Clicked 'Speichern' button at iframe level {level}")
            return True
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {i} at level {level}")
                if _recursive_click(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()
        return False

    print("🔍 Searching for 'Speichern' button...")
    time.sleep(1)  # Optional delay for safety
    result = _recursive_click(driver)
    if not result:
        print("❌ Could not find or click the 'Speichern' button.")
    return result
