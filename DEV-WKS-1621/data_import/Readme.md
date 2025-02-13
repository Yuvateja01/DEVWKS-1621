# Data Import to Webex

This folder contains Python scripts to automate the process of importing users and devices into Webex using the Webex API. The scripts read data from CSV files (`User.csv` and `Device.csv`), push the data to Webex, and generate a summary of the import operation.

## Features

### User Import (`webex_import.py`)
- Reads user data from `User.csv`.
- Pushes user data to Webex using the Webex API.
- Provides a detailed summary of the import operation, including successful and failed imports.

### Device Import (`add_device.py`)
- Reads device data from `Device.csv`.
- Pushes device data to Webex using the Webex API.
- Supports adding devices to a workspace or assigning them to a person.
- Provides a detailed summary of the import operation, including successful and failed imports.

## Directory Structure
```
data_import/ 
├── webex_import.py # Script for importing users to Webex 
├── add_device.py # Script for importing devices to Webex 
├── device_import_summary.json # Summary of the device import operation (generated after running add_device.py) 
├── import_summary.json # Summary of the user import operation (generated after running webex_import.py) 
└── README.md # Documentation for the data_import folder
```

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `csv`
  - `json`
- Webex API access token with the necessary permissions.

## How to Use

### 1. User Import
1. Place the `User.csv` file in the `../output_csv/` directory.
2. Update the `WEBEX_ACCESS_TOKEN` in `webex_import.py` with your Webex API access token.
3. Run the script:
   ```bash
   python webex_import.py```
4. Check the console output and the import_summary.json file for details of the import operation.

### 2. Device Import

1. Place the Device.csv file in the ../output_csv/ directory.
2. Update the WEBEX_ACCESS_TOKEN in add_device.py with your Webex API access token.
3. Run the script:
   ```bash
    python add_device.py```
4. Check the console output and the device_import_summary.json file for details of the import operation.

## Input File Formats
### User.csv
The User.csv file should contain the following columns:

    First Name: The first name of the user.
    Last Name: The last name of the user.
    Display Name: The display name of the user.
    User ID/Email (Required): The email address of the user.

### Device.csv
The Device.csv file should contain the following columns:

    MAC Address: The MAC address of the device.
    Model: The model of the device.
    Workspace ID: The ID of the workspace where the device will be created (optional).
    Person ID: The ID of the person who will own the device (optional).
    Password: SIP password for third-party devices (optional).

## Output Files

### User Import Summary (import_summary.json)

    Contains details of the user import operation, including:
        Total users processed.
        Number of successful imports.
        Number of failed imports.
        Details of each success and failure.

### Device Import Summary (device_import_summary.json)

    Contains details of the device import operation, including:
        Total devices processed.
        Number of successful imports.
        Number of failed imports.
        Details of each success and failure.


## Notes
    Ensure that the User.csv and Device.csv files are properly formatted and contain the required fields.
    The Webex API access token must have the necessary permissions to create users and devices.
    The scripts handle errors gracefully and provide detailed feedback in the summary files.

