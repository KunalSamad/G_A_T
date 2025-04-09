# File: features/verify_login_handler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def handle_second_login_page(driver, email, password, timeout=30):
    """
    Fills the second login (verification) page with email and password.
    Waits for user to manually solve captcha and submit the form.
    """
    try:
        print("🔐 Second login page detected. Filling email and password...")

        # Fill email
        try:
            email_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "0:form:usernameInput:topWrapper:inputWrapper:input"))
            )
            email_input.clear()
            email_input.send_keys(email)
        except TimeoutException:
            print("❌ Email field not found.")

        # Fill password
        try:
            password_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "id1"))
            )
            password_input.clear()
            password_input.send_keys(password)
        except TimeoutException:
            print("❌ Password field not found.")

        print("✅ Username and password filled. Please solve captcha manually and click 'Login'.")

    except Exception as e:
        print(f"⚠️ Error filling second login: {e}")
