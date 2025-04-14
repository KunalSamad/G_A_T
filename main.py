# File: main.py

from utils.credential_csv_loader import load_formatted_credentials
from browser.browser_launcher import create_browser
from features.login_handler import login_to_gmx
from features.verify_login_handler import handle_second_login_page
from features.navigate_to_settings import go_to_settings_page
from features.navigate_to_verteiler import extract_verteiler_href
from features.popup_handler import handle_consent_popup
from features.verteiler.open_creator_form import open_verteiler_creator
from features.verteiler.name_filler import fill_verteiler_name
from features.verteiler.address_extractor import extract_verteiler_email_address  # ✅ NEW IMPORT

import time

# Step 1: Load credentials
credentials = load_formatted_credentials("output/loaded_credentials.csv")

if not credentials:
    print("No credentials loaded. Please check your CSV file.")
    exit()

# Step 2: Launch browser
print("Launching browser...")
driver = create_browser()
driver.get("https://www.gmx.net")

# Step 3A: Try to handle consent popup after initial load
handle_consent_popup(driver)

# Step 4: Login to GMX with first account
first_credential = credentials[0]
email = first_credential["email"]
password = first_credential["password"]
login_to_gmx(driver, email, password)

# Step 5: Check if second login (verification) is needed
print("⏳ Waiting briefly to check for second login page...")
time.sleep(5)

if "verify.login.gmx.net" in driver.current_url:
    handle_second_login_page(driver, email, password)
    input("📌 Please complete CAPTCHA and press Enter to continue...")
else:
    print("✅ No second login required. Continuing...")

# Step 5B: Check again for popup after login
handle_consent_popup(driver)

# Step 6: Navigate to settings
go_to_settings_page(driver)

# Step 7: Use CDP sniffing to extract Verteiler URL
verteiler_url = extract_verteiler_href(driver)
if verteiler_url:
    driver.get(verteiler_url)
    print("🟢 Successfully opened Verteiler page via CDP sniffing.")
else:
    print("❌ Could not open Verteiler page. You may try manually navigating.")

# Step 8: Click "Neuen Verteiler anlegen"
open_verteiler_creator(driver)

# Step 9: Fill Verteiler list name
kun_number = 2  # This should eventually be dynamic
fill_verteiler_name(driver, kun_number)

# ✅ Step 10: Extract Verteiler email address
verteiler_email = extract_verteiler_email_address(driver)
if verteiler_email:
    print(f"📬 Extracted Verteiler address: {verteiler_email}")
    # TODO: Store to CSV here
else:
    print("⚠️ Verteiler address not found.")

# Step End of Flow
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
