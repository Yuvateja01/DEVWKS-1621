# CUCM Configuration Export Tool

This tool is designed to extract configuration data from Cisco Unified Communications Manager (CUCM) using the AXL API. It retrieves data for Phones, Users, and Lines, processes it, and saves the results in JSON format.

## Features

- **Phone Configuration**: Retrieves phone configurations filtered by `devicePoolName` and saves the full configuration for each phone.
- **User Configuration**: Extracts `ownerUserName` from phone configurations and retrieves the corresponding user details.
- **Line Configuration**: Extracts unique `pattern` and `routePartitionName` combinations from phone configurations and retrieves the corresponding line details.
- **Progress Tracking**: Uses `tqdm` to display progress bars for long-running operations.
- **Error Handling**: Handles errors gracefully, ensuring the script continues even if some entries fail.

## Directory Structure
```
ConfigExports/ 
└── <siteCode>/ 
├── Phone.json # Contains full phone configurations 
├── User.json # Contains user configurations 
└── Line.json # Contains line configurations
```

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `tqdm`
  - `os`
  - `json`
  - `traceback`
- Access to CUCM with AXL API enabled.
- Proper credentials and permissions to access CUCM data.

## How It Works

1. **CUCM Connectivity Check**:
   - The script verifies connectivity to CUCM using the `check_cucm` method.
   - If connectivity fails, the script exits with an error message.

2. **Phone Data Extraction**:
   - The script uses the `listPhone` method to retrieve a list of phones filtered by `devicePoolName`.
   - For each phone, the `getPhone` method retrieves the full configuration.
   - The results are saved to `Phone.json`.

3. **User Data Extraction**:
   - The script reads `Phone.json` to extract unique `ownerUserName` values.
   - For each `ownerUserName`, the `getUser` method retrieves the user configuration.
   - The results are saved to `User.json`.

4. **Line Data Extraction**:
   - The script reads `Phone.json` to extract unique `pattern` and `routePartitionName` combinations.
   - For each combination, the `getLine` method retrieves the line configuration.
   - The results are saved to `Line.json`.

5. **Progress Tracking**:
   - The `tqdm` library is used to display progress bars for fetching phone, user, and line configurations.

## How to Run

1. Clone or download the repository containing this script.
2. Ensure the required Python libraries are installed.
3. Update the `ucmSourceContent` and `ucm_source` objects with your CUCM credentials and connection details.
4. Run the script using the following command:

   ```bash
   python <script_name>.py

5. The extracted data will be saved in the ConfigExports/<siteCode> directory.

## Error Handling

    If any errors occur during data retrieval (e.g., invalid credentials, missing data), the script logs the error and continues processing the remaining entries.
    Ensure that the CUCM AXL API is enabled and accessible.

## Notes

    Ensure that the devicePoolName filter in the configList dictionary is updated to match your CUCM environment.
    The script assumes that the write_results method is implemented to save data to JSON files.

