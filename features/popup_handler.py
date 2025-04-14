# File: features/popup_handler.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time

def _click_button_by_text_js(driver: WebDriver, target_text: str) -> bool:
    script = f"""
    const elements = document.querySelectorAll('*');
    for (const el of elements) {{
        const style = window.getComputedStyle(el);
        const visible = style && style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
        if (visible && el.innerText.trim() === "{target_text}") {{
            el.click();
            return true;
        }}
    }}
    return false;
    """
    return driver.execute_script(script)

def _search_iframes_recursively(driver: WebDriver, level=0, text="Akzeptieren und weiter") -> bool:
    indent = "  " * level
    try:
        if _click_button_by_text_js(driver, text):
            print(f"{indent}✅ Consent button clicked at iframe level {level}")
            return True
    except Exception:
        pass

    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"{indent}🔍 Found {len(iframes)} iframe(s) at level {level}")
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                print(f"{indent}➡️ Entering iframe {index} at level {level}")
                if _search_iframes_recursively(driver, level + 1, text):
                    return True
                driver.switch_to.parent_frame()
            except Exception:
                driver.switch_to.parent_frame()
    except Exception:
        pass

    return False

def handle_consent_popup(driver: WebDriver, timeout: int = 10) -> bool:
    print("⏳ Waiting briefly for popup rendering...")
    time.sleep(timeout)
    print("🔍 Searching for GMX consent popup...")
    try:
        driver.switch_to.default_content()
        found = _search_iframes_recursively(driver)
        if found:
            print("✅ Consent popup handled successfully.")
        else:
            print("❌ Consent popup not found.")
        return found
    except Exception as e:
        print(f"⚠️ Error handling consent popup: {e}")
        return False
