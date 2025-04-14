# File: features/verteiler/fill_list_info.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def fill_verteiler_name(driver, kun_number):
    """
    Fills the Verteiler name field with kunX where X = kun_number.
    """
    try:
        print(f"✏️ Entering Verteiler name: kun{kun_number}")
        name_field = driver.find_element(By.CSS_SELECTOR, 'input[data-webdriver="name"]')
        name_field.clear()
        name_field.send_keys(f"kun{kun_number}")
        return True
    except Exception as e:
        print(f"❌ Failed to fill Verteiler name: {e}")
        return False
