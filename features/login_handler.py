# File: features/login_handler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login_to_gmx(driver, email, password, timeout=15):
    """
    Logs into GMX using provided email and password.
    Assumes the browser is already on https://www.gmx.net
    """
    try:
        print(f"🔐 Attempting login for: {email}")

        # Wait for email input to appear
        email_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "mailInput"))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Wait for password input to appear
        password_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "pwInput"))
        )
        password_input.clear()
        password_input.send_keys(password)

        # Click the login button
        login_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "form[data-form-login] button[type='submit']"))
        )
        login_button.click()

        print("🚀 Login submitted.")

    except TimeoutException:
        print("❌ Login fields not found or took too long to appear.")
    except Exception as e:
        print(f"⚠️ Login error: {e}")
