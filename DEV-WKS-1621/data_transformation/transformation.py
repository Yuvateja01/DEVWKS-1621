# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28, 2025

@description: This script transforms JSON files (Phone, User, DirectoryNumber) into CSV files
              by extracting specific fields and saving them in a structured format.

@usage: Place this script in the `data_transformation` folder and run it to generate CSV files.
"""

import os
import json
import csv
import sys
sys.path.append("../")


# Define input and output directories
file_path = "./data_collection/adapter/source.json"
siteCode = json.load(open(file_path, "r"))["siteCode"]
INPUT_DIR = f"./ConfigExports/{siteCode}/"
OUTPUT_DIR = "./OutputCSV/"

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def read_json(file_path):
    """
    Reads a JSON file and returns its content as a Python object.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list/dict: Parsed JSON content.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None

def write_csv(file_path, data, headers):
    """
    Writes data to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data (list of dict): Data to write to the CSV file.
        headers (list): List of column headers for the CSV file.
    """
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV file created: {file_path}")
    except Exception as e:
        print(f"Error writing CSV file {file_path}: {e}")

def transform_users(input_file, output_file):
    """
    Transforms User JSON data into a CSV file with specific fields.

    Args:
        input_file (str): Path to the User JSON file.
        output_file (str): Path to the output CSV file.
    """
    data = read_json(input_file)
    if not data:
        return

    # Extract specific fields
    transformed_data = []
    for user in data:
        transformed_data.append({
            "First Name": user.get("firstName", ""),
            "Last Name": user.get("lastName", ""),
            "Display Name": f"{user.get('displayName', '')}",
            "User ID/Email (Required)": user.get("userid", ""),
            "Extension": user.get("primaryExtension", ""),
            "Phone Number": user.get("primaryExtension", ""),
            "Caller ID Number": user.get("primaryExtension", ""),
            "Caller ID First Name": user.get("firstName", ""),
            "Caller ID Last Name": user.get("lastName", ""),
            "Location": siteCode
        })

    # Define CSV headers
    headers = [
        "First Name", "Last Name", "Display Name", "User ID/Email (Required)",
        "Extension", "Phone Number", "Caller ID Number", "Caller ID First Name",
        "Caller ID Last Name", "Location"
    ]

    # Write to CSV
    write_csv(output_file, transformed_data, headers)

def transform_phones(input_file, output_file):
    """
    Transforms Phone JSON data into a CSV file with specific fields.

    Args:
        input_file (str): Path to the Phone JSON file.
        output_file (str): Path to the output CSV file.
    """
    data = read_json(input_file)
    if not data:
        return

    # Extract specific fields
    transformed_data = []
    for phone in data:
        if phone.get("lines"):
            lines = phone.get("lines", {}).get("line", [{}])[0].get("dirn", {}).get("pattern", "")
        transformed_data.append({
            "Username": phone.get("ownerUserName", ""),
            "Type": phone.get("type", "USER"),
            "Extension": lines,
            "Phone Number": lines,
            "Device Type": phone.get("deviceType", "IP"),
            "Model": phone.get("model", ""),
            "MAC Address": phone.get("name", "").strip("SEP"),
            "Location": phone.get("devicePoolName", "")
        })

    # Define CSV headers
    headers = [
        "Username", "Type", "Extension", "Phone Number", "Device Type",
        "Model", "MAC Address", "Location"
    ]

    # Write to CSV
    write_csv(output_file, transformed_data, headers)

def transform_directory_numbers(input_file, output_file):
    """
    Transforms DirectoryNumber JSON data into a CSV file with specific fields.

    Args:
        input_file (str): Path to the DirectoryNumber JSON file.
        output_file (str): Path to the output CSV file.
    """
    data = read_json(input_file)
    if not data:
        return

    # Extract specific fields
    transformed_data = [{"Number": dn.get("pattern", "")} for dn in data]

    # Define CSV headers
    headers = ["Number"]

    # Write to CSV
    write_csv(output_file, transformed_data, headers)

def main():
    """
    Main function to execute the transformation process.
    """
    try:
        # File paths
        phone_json = os.path.join(INPUT_DIR, "phone.json")
        user_json = os.path.join(INPUT_DIR, "user.json")
        directory_number_json = os.path.join(INPUT_DIR, "line.json")

        phone_csv = os.path.join(OUTPUT_DIR, "Phone.csv")
        user_csv = os.path.join(OUTPUT_DIR, "User.csv")
        directory_number_csv = os.path.join(OUTPUT_DIR, "DirectoryNumber.csv")

        # Transform JSON to CSV
        print("Transforming User JSON to CSV...")
        transform_users(user_json, user_csv)

        print("Transforming Phone JSON to CSV...")
        transform_phones(phone_json, phone_csv)

        print("Transforming DirectoryNumber JSON to CSV...")
        transform_directory_numbers(directory_number_json, directory_number_csv)

        print("\nTransformation completed successfully!")

    except Exception as e:
        print("Error occurred during transformation:", str(e))

if __name__ == "__main__":
    main()
