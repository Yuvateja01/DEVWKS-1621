# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28, 2025

@description: This script reads Device.csv, pushes devices to Webex using the Webex API,
              and provides a summary of the operation.

@usage: Place this script in the `Data_import` folder and run it to add devices to Webex.
"""

import csv
import json
import requests

# Define constants
DEVICE_CSV_FILE = "./OutputCSV/Phone.csv"  # Path to the Device.csv file
WEBEX_API_URL = "https://webexapis.com/v1/devices"  # Webex API endpoint for adding devices
WEBEX_API_URL_PEOPLE = "https://webexapis.com/v1/people"  # Webex API endpoint for people
OUTPUT_SUMMARY_FILE = "./device_import_summary.json"  # Path to save the summary

with open("./data_import/config.json", "r") as file:
    config = json.load(file)
    WEBEX_ACCESS_TOKEN = config["WEBEX_ACCESS_TOKEN"]
    ORGANIZATION_ID = config["ORGANIZATION_ID"]
    DOMAIN = config["DOMAIN"]
    WORKSPACE_ID = config["WORKSPACE_ID"]

WEBEX_API_URL = f"{WEBEX_API_URL}?orgId={ORGANIZATION_ID}"

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

def get_person_id(email):
    """
    Retrieves the person ID for a given email address.

    Args:
        email (str): Email address of the user.

    Returns:
        str: Person ID if found, otherwise an empty string.
    """
    url = f"{WEBEX_API_URL_PEOPLE}?email={email}"
    try:
        print("Getting person ID for", email)
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if data.get("items"):
            return data["items"][0]["id"]
        return ""
    except Exception as e:
        print(f"Error retrieving person ID for {email}: {e}")

def push_device_to_webex(device):
    """
    Pushes a single device to Webex using the Webex API.

    Args:
        device (dict): Device data to push.

    Returns:
        dict: Response from the Webex API.
    """
    email = device.get("Username", None)
    if email:
        if "@" not in email:
            email = f"{email}@{DOMAIN}"
            person_id = get_person_id(email)
            # print(person_id)
        else:
            person_id = get_person_id(email)
    else:
        person_id = None
    print(person_id)
    if person_id:
        payload = {
            "mac": device.get("MAC Address", ""),
            "model": device.get("Model", ""),
            "personId": person_id,
            # "password": device.get("Password", "12345678")  # Optional, only for third-party devices
        }
    else:
        payload = {
            "mac": device.get("MAC Address", ""),
            "model": device.get("Model", ""),
            "workspaceId": WORKSPACE_ID,
        }

    # Remove empty fields from the payload
    payload = {key: value for key, value in payload.items() if value}

    try:
        response = requests.post(WEBEX_API_URL, headers=HEADERS, data=json.dumps(payload))
        return response.json()
    except Exception as e:
        print(f"Error pushing device {device.get('MAC Address', '')} to Webex: {e}")
        return {"error": str(e)}

def import_devices_to_webex(device_data):
    """
    Imports all devices from the provided device data to Webex.

    Args:
        device_data (list): List of device data dictionaries.

    Returns:
        dict: Summary of the import operation.
    """
    summary = {
        "total_devices": len(device_data),
        "success_count": 0,
        "failure_count": 0,
        "success_devices": [],
        "failed_devices": []
    }

    for device in device_data:
        response = push_device_to_webex(device)
        if "id" in response:  # Successful response contains an 'id'
            summary["success_count"] += 1
            summary["success_devices"].append({
                "mac": device.get("MAC Address", ""),
                "response": response
            })
        else:
            summary["failure_count"] += 1
            summary["failed_devices"].append({
                "mac": device.get("MAC Address", ""),
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
    Main function to execute the Webex device import process.
    """
    try:
        # Read device data from Device.csv
        device_data = read_csv(DEVICE_CSV_FILE)
        if not device_data:
            print("No device data found. Exiting.")
            return

        # Import devices to Webex
        print("Importing devices to Webex...")
        summary = import_devices_to_webex(device_data)

        # Write summary to file
        write_summary_to_file(summary, OUTPUT_SUMMARY_FILE)

        # Print summary
        print("\nImport Summary:")
        print(f"Total Devices: {summary['total_devices']}")
        print(f"Successfully Imported: {summary['success_count']}")
        print(f"Failed Imports: {summary['failure_count']}")

    except Exception as e:
        print("Error occurred during Webex device import:", str(e))

if __name__ == "__main__":
    main()
