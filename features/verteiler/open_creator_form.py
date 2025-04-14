# File: features/verteiler/open_creator_form.py

from selenium.webdriver.common.by import By
import time

def open_verteiler_creator(driver):
    """
    Searches through all iframes to find and click the 'Neuen Verteiler anlegen' button.
    Returns True if clicked successfully.
    """
    def recursive_iframe_search(level=0):
        indent = "  " * level
        try:
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-webdriver="createDistributionListButton"]')
            button.click()
            print(f"{indent}✅ Clicked 'Neuen Verteiler anlegen' button at iframe level {level}")
            return True
        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {index} at level {level}")
                if recursive_iframe_search(level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return False

    print("🔍 Searching for 'Neuen Verteiler anlegen' button...")
    success = recursive_iframe_search()

    if not success:
        print("❌ Could not find or click the 'Neuen Verteiler anlegen' button.")
    return success
