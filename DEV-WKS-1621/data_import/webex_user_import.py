# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28, 2025

@description: This script reads User.csv, pushes users to Webex using the Webex API,
              and provides a summary of the operation.

@usage: Place this script in the `Data_import` folder and run it to import users to Webex.
"""

import csv
import json
import requests
import sys
sys.path.append("../")

# Define constants
USER_CSV_FILE = "./OutputCSV/User.csv"  # Path to the User.csv file
WEBEX_API_URL = "https://webexapis.com/v1/people"  # Webex API endpoint
OUTPUT_SUMMARY_FILE = "./import_summary.json"  # Path to save the summary

with open("./data_import/config.json", "r") as file:
    config = json.load(file)
    WEBEX_ACCESS_TOKEN = config["WEBEX_ACCESS_TOKEN"]
    ORGANIZATION_ID = config["ORGANIZATION_ID"]
    DOMAIN = config["DOMAIN"]

# Headers for Webex API requests
HEADERS = {
    "Authorization": f"Bearer {WEBEX_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def read_csv(file_path):
    """
    Reads a CSV file and returns its content as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries representing the rows in the CSV file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return []

def push_user_to_webex(user):
    """
    Pushes a single user to Webex using the Webex API.

    Args:
        user (dict): User data to push.

    Returns:
        dict: Response from the Webex API.
    """
    email = user.get("User ID/Email (Required)", "")
    if "@" not in email:
        email = f"{email}@{DOMAIN}"

    payload = {
        "emails": [email],
        "firstName": user.get("First Name", ""),
        "lastName": user.get("Last Name", ""),
        "displayName": user.get("Display Name", ""),
        "orgId": ORGANIZATION_ID,
    }

    try:
        response = requests.post(WEBEX_API_URL, headers=HEADERS, data=json.dumps(payload))
        return response.json()
    except Exception as e:
        print(f"Error pushing user {user.get('User ID/Email (Required)', '')} to Webex: {e}")
        return {"error": str(e)}

def import_users_to_webex(user_data):
    """
    Imports all users from the provided user data to Webex.

    Args:
        user_data (list): List of user data dictionaries.

    Returns:
        dict: Summary of the import operation.
    """
    summary = {
        "total_users": len(user_data),
        "success_count": 0,
        "failure_count": 0,
        "success_users": [],
        "failed_users": []
    }

    for user in user_data:
        response = push_user_to_webex(user)
        if "id" in response:  # Successful response contains an 'id'
            summary["success_count"] += 1
            summary["success_users"].append({
                "email": user.get("User ID/Email (Required)", ""),
                "response": response
            })
        else:
            summary["failure_count"] += 1
            summary["failed_users"].append({
                "email": user.get("User ID/Email (Required)", ""),
                "response": response
            })

    return summary

def write_summary_to_file(summary, file_path):
    """
    Writes the summary of the import operation to a JSON file.

    Args:
        summary (dict): Summary data to write.
        file_path (str): Path to the output file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4)
        print(f"Summary written to {file_path}")
    except Exception as e:
        print(f"Error writing summary to file {file_path}: {e}")

def main():
    """
    Main function to execute the Webex user import process.
    """
    try:
        # Read user data from User.csv
        user_data = read_csv(USER_CSV_FILE)
        if not user_data:
            print("No user data found. Exiting.")
            return

        # Import users to Webex
        print("Importing users to Webex...")
        summary = import_users_to_webex(user_data)

        # Write summary to file
        write_summary_to_file(summary, OUTPUT_SUMMARY_FILE)

        # Print summary
        print("\nImport Summary:")
        print(f"Total Users: {summary['total_users']}")
        print(f"Successfully Imported: {summary['success_count']}")
        print(f"Failed Imports: {summary['failure_count']}")

    except Exception as e:
        print("Error occurred during Webex user import:", str(e))

if __name__ == "__main__":
    main()
