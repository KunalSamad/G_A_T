# File: utils/credential_csv_loader.py
import csv
import os

def load_formatted_credentials(filepath):
    """
    Loads structured credentials from a CSV file and returns them as a list of dictionaries.
    Each row must have 'email' and 'password' headers.
    """
    credentials = []
    if not os.path.exists(filepath):
        print(f"Credential CSV file not found at path: {filepath}")
        return credentials

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                email = row.get("email")
                password = row.get("password")
                if email and password:
                    credentials.append({"email": email, "password": password})
                else:
                    print(f"Invalid row skipped: {row}")
    except Exception as e:
        print(f"Error reading CSV credentials: {e}")

    return credentials

if __name__ == "__main__":
    path = "C:/GMX_Automation_Tool/Output/loaded_credentials.csv"
    accounts = load_formatted_credentials(path)
    print("\nLoaded Credentials:")
    for index, acc in enumerate(accounts, start=1):
        print(f"{index}. Email: {acc['email']} | Password: {acc['password']}")
