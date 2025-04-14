# File: main.py

from utils.credential_csv_loader import load_formatted_credentials
from browser.browser_launcher import create_browser
from features.login_handler import login_to_gmx
from features.verify_login_handler import handle_second_login_page
from features.navigate_to_settings import go_to_settings_page
from features.navigate_to_verteiler import extract_verteiler_href
from selenium.webdriver.support.ui import WebDriverWait
import time

# Step 1: Load credentials
credentials = load_formatted_credentials("output/loaded_credentials.csv")

if not credentials:
    print("No credentials loaded. Please check your CSV file.")
    exit()

# Step 2: Launch browser
print("Launching browser...")
driver = create_browser()
driver.get("https://www.gmx.net")  # This will likely redirect to /consent-management

# Step 3: Let user manually pass consent
print("🌐 Waiting for user to manually accept GMX consent...")
try:
    WebDriverWait(driver, 120).until(
        lambda d: d.current_url == "https://www.gmx.net/" or ("gmx.net" in d.current_url and "consent-management" not in d.current_url)
    )
    print("✅ Consent passed, continuing with login automation...")
except:
    print("⚠️ Timeout or error waiting for consent. Login skipped.")

# Step 4: Login to GMX with first account
first_credential = credentials[0]
email = first_credential["email"]
password = first_credential["password"]
login_to_gmx(driver, email, password)

# Step 5: Detect if second login page appears
print("⏳ Waiting briefly to check for second login page...")
time.sleep(5)  # allow redirect if necessary

if "verify.login.gmx.net" in driver.current_url:
    handle_second_login_page(driver, email, password)
    input("📌 Please complete CAPTCHA and press Enter to continue...")
else:
    print("✅ No second login required. Continuing...")

# Step 6: Navigate to settings page
go_to_settings_page(driver)

# Step 7: Use DevTools log to sniff Verteiler page link
verteiler_url = extract_verteiler_href(driver)
if verteiler_url:
    driver.get(verteiler_url)
    print("🟢 Successfully opened Verteiler page via CDP sniffing.")
else:
    print("❌ Could not open Verteiler page. You may try manually navigating.")

# Step 8: Keep browser open for user to interact or develop
print("\n🟢 Login and navigation to Verteiler completed. You may now interact with the browser manually.")
print("🔒 Press Ctrl+C to stop the script when ready.")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n🛑 Script manually stopped.")
finally:
    try:
        driver.quit()
    except:
        pass
