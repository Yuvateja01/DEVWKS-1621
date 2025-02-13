# Data Transformation Tool

This repository contains a Python script (`transformation.py`) that transforms JSON files into CSV files by extracting specific fields. It is designed to process configuration data exported from Cisco Unified Communications Manager (CUCM) and convert it into a structured format for further analysis or reporting.

## Features

- **Transforms JSON to CSV**: Converts `Phone.json`, `User.json`, and `DirectoryNumber.json` into corresponding CSV files.
- **Field Extraction**: Extracts only the required fields from each JSON file for better usability.
- **Modular Design**: The script is modular, making it easy to extend or modify.
- **Error Handling**: Handles errors gracefully during file reading, writing, and transformation.

## Directory Structure
```
data_transformation/ 
├── transformation.py # Main script for JSON to CSV transformation 
├── output_csv/ # Directory where the generated CSV files are saved 
└── README.md # Documentation for the repository
```

## Input and Output

### Input Files
The script expects the following JSON files as input:
1. **Phone.json**: Contains phone configuration data.
2. **User.json**: Contains user configuration data.
3. **DirectoryNumber.json**: Contains directory number data.

### Output Files
The script generates the following CSV files:
1. **Phone.csv**: Extracted fields from `Phone.json`.
2. **User.csv**: Extracted fields from `User.json`.
3. **DirectoryNumber.csv**: Extracted fields from `DirectoryNumber.json`.

## Extracted Fields

### User Fields
The following fields are extracted from `User.json`:
- First Name
- Last Name
- Display Name
- User ID/Email (Required)
- Extension
- Phone Number
- Caller ID Number
- Caller ID First Name
- Caller ID Last Name
- Location

### Phone Fields
The following fields are extracted from `Phone.json`:
- Username
- Type
- Extension
- Phone Number
- Device Type
- Model
- MAC Address
- Location

### Directory Number Fields
The following field is extracted from `DirectoryNumber.json`:
- Number

## How to Use

1. **Place Input Files**:
   - Ensure the JSON files (`Phone.json`, `User.json`, `DirectoryNumber.json`) are located in the `../ConfigExports/` directory relative to the script.

2. **Run the Script**:
   - Execute the script using the following command:
     ```bash
     python transformation.py
     ```

3. **Check Output**:
   - The generated CSV files will be saved in the `output_csv/` directory.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `os`
  - `json`
  - `csv`

## Example Output

### User.csv
```csv
First Name,Last Name,Display Name,User ID/Email (Required),Extension,Phone Number,Caller ID Number,Caller ID First Name,Caller ID Last Name,Location
John,Doe,John Doe,john.doe@example.com,1234,555-1234,555-1234,John,Doe,New York


## Notes

    Ensure the input JSON files are properly formatted and contain the required fields.
    The script assumes the JSON files are exported from CUCM and follow the expected structure.
