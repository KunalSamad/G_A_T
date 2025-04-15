# File: main.py

from utils.credential_csv_loader import load_formatted_credentials
from utils.email_loader import load_emails
from browser.browser_launcher import create_browser
from features.login_handler import login_to_gmx
from features.verify_login_handler import handle_second_login_page
from features.navigate_to_settings import go_to_settings_page
from features.navigate_to_verteiler import extract_verteiler_href
from features.popup_handler import handle_consent_popup
from features.verteiler.open_creator_form import open_verteiler_creator
from features.verteiler.name_filler import fill_verteiler_name
from features.verteiler.address_extractor import extract_verteiler_email_address
from features.verteiler.email_inserter import insert_emails_to_verteiler
from features.verteiler.select_permission_mode import select_jeder_option
from features.verteiler.save_button_clicker import click_speichern_button  # ✅ NEW

import time

# Step 1: Load credentials and emails
credentials = load_formatted_credentials("output/loaded_credentials.csv")
email_list = load_emails("Output/data_ids.txt")

if not credentials:
    print("No credentials loaded. Please check your CSV file.")
    exit()

# Step 2: Launch browser
print("Launching browser...")
driver = create_browser()
driver.get("https://www.gmx.net")

# Step 3: Handle initial consent popup
handle_consent_popup(driver)

# Step 4: Login to GMX with first account
first_credential = credentials[0]
email = first_credential["email"]
password = first_credential["password"]
login_to_gmx(driver, email, password)

# Step 5: Handle second login if required
print("⏳ Waiting briefly to check for second login page...")
time.sleep(5)

if "verify.login.gmx.net" in driver.current_url:
    handle_second_login_page(driver, email, password)
    input("📌 Please complete CAPTCHA and press Enter to continue...")
else:
    print("✅ No second login required. Continuing...")

# Step 6: Handle possible consent popup after login
handle_consent_popup(driver)

# Step 7: Navigate to settings
go_to_settings_page(driver)

# Step 8: Sniff and open Verteiler page
verteiler_url = extract_verteiler_href(driver)
if verteiler_url:
    driver.get(verteiler_url)
    print("🟢 Successfully opened Verteiler page via CDP sniffing.")
else:
    print("❌ Could not open Verteiler page. You may try manually navigating.")

# Step 9: Click 'Neuen Verteiler anlegen'
open_verteiler_creator(driver)

# Step 10: Fill Verteiler name
kun_number = 1  # TODO: Make dynamic later
fill_verteiler_name(driver, kun_number)

# Step 11: Extract and log Verteiler email address
verteiler_email = extract_verteiler_email_address(driver)
if verteiler_email:
    print(f"📬 Extracted Verteiler address: {verteiler_email}")
    # TODO: Save to CSV
else:
    print("⚠️ Verteiler address not found.")

# Step 12: Insert email addresses
insert_emails_to_verteiler(driver, email_list[:50])  # First 50 emails

# Step 13: Select "Jeder" from dropdown
select_jeder_option(driver)

# ✅ Step 14: Click 'Speichern' button
click_speichern_button(driver)

# ✅ Final Message
print("\n🟢 Verteiler creation completed. You may now interact with the browser manually.")
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
