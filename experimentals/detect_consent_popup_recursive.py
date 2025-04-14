# File: detect_consent_popup_recursive.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def connect_to_existing_browser():
    chrome_options = Options()
    chrome_options.debugger_address = "localhost:9222"
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def execute_js_click(driver, search_text):
    js = f"""
    const elements = document.querySelectorAll('*');
    for (const el of elements) {{
        const style = window.getComputedStyle(el);
        const visible = style && style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
        if (visible && el.innerText.trim() === "{search_text}") {{
            el.click();
            return true;
        }}
    }}
    return false;
    """
    return driver.execute_script(js)

def search_iframes_recursively(driver, level=0):
    indent = "  " * level
    print(f"{indent}🔎 Searching level {level} iframe(s)...")

    try:
        if execute_js_click(driver, "Akzeptieren und weiter"):
            print(f"{indent}✅ Found and clicked the consent button!")
            return True
    except Exception:
        pass

    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"{indent}➡️ Found {len(iframes)} iframe(s) at level {level}")

        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}🔁 Entering iframe {index} at level {level}")
                if search_iframes_recursively(driver, level + 1):
                    return True
                driver.switch_to.parent_frame()
            except Exception as e:
                print(f"{indent}⚠️ Failed to enter iframe {index} at level {level}: {e}")
                driver.switch_to.parent_frame()
    except Exception as e:
        print(f"{indent}⚠️ Failed to list iframes at level {level}: {e}")

    return False

if __name__ == "__main__":
    print("✅ Connecting to running Chrome session...")
    driver = connect_to_existing_browser()
    print(f"🌐 Current page: {driver.current_url}")

    input("📌 Open https://www.gmx.net and press Enter when the popup is visible...")

    print("⏳ Starting recursive iframe search for consent button...")
    found = search_iframes_recursively(driver)

    if not found:
        print("❌ Could not find consent button, even recursively.")
        print("⚠️ Please handle the popup manually.")
