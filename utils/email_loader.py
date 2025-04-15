# File: utils/email_loader.py

def load_emails(filepath):
    """Loads email addresses from a text file, one per line."""
    emails = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                email = line.strip()
                if email:
                    emails.append(email)
        print(f"✅ Loaded {len(emails)} emails from: {filepath}")
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"⚠️ Error while loading emails: {e}")
    return emails
