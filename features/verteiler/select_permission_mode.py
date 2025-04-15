# File: features/verteiler/select_permission_mode.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
import time

def select_jeder_option(driver: WebDriver):
    """
    Recursively traverses iframes to locate the Verteiler permission dropdown
    and selects the 'Jeder (öffentlich)' option.
    """
    def recursive_select(driver, level=0):
        indent = "  " * level
        try:
            dropdown = Select(driver.find_element(By.NAME, "fieldset:modeDropDown"))
            dropdown.select_by_visible_text("Jeder (öffentlich)")
            print(f"{indent}✅ Selected 'Jeder (öffentlich)' at level {level}")
            return True
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for idx, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {idx} at level {level}")
                if recursive_select(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return False

    print("🔽 Looking for dropdown to set reply permission to 'Jeder'...")
    result = recursive_select(driver)
    if not result:
        print("❌ Could not locate or update the dropdown for permission mode.")
    return result
