# File: features/navigate_to_settings.py

from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs


def go_to_settings_page(driver, timeout=60):
    """
    Extracts the session ID (sid) from the current URL and uses it to
    navigate to the GMX Settings page for Verteiler management.
    """
    try:
        print("⏳ Attempting to retrieve session ID (sid) from URL after login...")

        WebDriverWait(driver, timeout).until(lambda d: "sid=" in d.current_url)
        url = driver.current_url
        parsed_url = urlparse(url)
        sid = parse_qs(parsed_url.query).get("sid", [None])[0]

        if sid:
            settings_url = f"https://bap.navigator.gmx.net/mail_settings?sid={sid}"
            driver.get(settings_url)
            print("⚙️  Navigated to GMX Settings page.")
        else:
            print("❌ Could not extract session ID (sid) from URL.")

    except Exception as e:
        print(f"⚠️ Error navigating to settings: {e}")