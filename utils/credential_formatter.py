# File: utils/credential_formatter.py
import csv
import os

def format_raw_credentials(filepath):
    """
    Loads raw credentials from a text file and writes them to a CSV file in a structured format.
    Each line in the input file should be formatted as:
    email----password----(optional phone)
    """
    credentials = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("----")
                if len(parts) >= 2:
                    email, password = parts[0], parts[1]
                    credentials.append({
                        "email": email,
                        "password": password
                    })
                else:
                    print(f"Invalid line skipped: {line.strip()}")
    except FileNotFoundError:
        print(f"Credential file not found at path: {filepath}")
        return
    except Exception as e:
        print(f"Error reading credentials: {e}")
        return

    output_dir = r"C:\GMX_Automation_Tool\Output"
    output_file = os.path.join(output_dir, "loaded_credentials.csv")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["email", "password"])
            writer.writeheader()
            for entry in credentials:
                writer.writerow(entry)
        print(f"\nFormatted credentials written to: {output_file}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    filepath = r"C:\GMX_Automation_Tool\data\credentials.txt"
    format_raw_credentials(filepath)
