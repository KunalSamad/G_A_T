# File: features/verteiler/email_inserter.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

def insert_emails_to_verteiler(driver: WebDriver, email_list: list[str]) -> bool:
    """
    Recursively searches for the email input field and inserts all emails.
    Returns True if successful, False otherwise.
    """
    print("📩 Attempting to insert emails into Verteiler field...")

    def recursive_insert(driver, level=0):
        indent = "  " * level
        try:
            input_field = driver.find_element(By.CSS_SELECTOR, "input.select2-input")
            input_text = ", ".join(email_list)  # Insert all at once, separated by commas
            input_field.send_keys(input_text)
            input_field.send_keys(Keys.ENTER)
            print(f"{indent}✅ Inserted {len(email_list)} emails successfully at level {level}.")
            return True
        except:
            pass

        # Check child iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {i} at level {level}")
                if recursive_insert(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except:
                driver.switch_to.parent_frame()

        return False

    success = recursive_insert(driver)
    if not success:
        print("❌ Could not locate or insert emails into the field.")
    return success
