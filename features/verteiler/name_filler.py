# File: features/verteiler/name_filler.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def fill_verteiler_name(driver: WebDriver, kun_number: int) -> bool:
    """
    Recursively traverses iframes to locate the Verteiler name field and fill it with 'kun{kun_number}'.
    Returns True if successful, False otherwise.
    """

    print("⏳ Waiting for Verteiler form to load...")
    time.sleep(3)  # Allow time for input box to render

    def _recursive_search(driver, level=0):
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
                if _recursive_search(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return False

    print("🔍 Searching recursively for Verteiler name field...")
    result = _recursive_search(driver)
    if not result:
        print("❌ Could not find or fill the Verteiler name field.")
    return result
