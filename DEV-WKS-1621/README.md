# DEVWKS_AMS_2025

Welcome to the DEVWKS_AMS_2025 project! This repository contains materials and resources for the Cisco Live EMEA 2025 workshop.

Based on the provided content, I'll help create a comprehensive README.md for the source folder that encompasses all three components. Here's the README.md code:

# CUCM to Webex Migration Tool

This repository contains a suite of tools designed to facilitate the migration of configurations from Cisco Unified Communications Manager (CUCM) to Webex. The process is divided into three main components: data collection, transformation, and import.

## Repository Structure

```
sourcefolder/
├── data_collection/     # CUCM configuration export tools
├── data_transformation/ # JSON to CSV transformation tools
├── data_import/        # Webex import tools
└── README.md           # This file
```

## Components

### 1. Data Collection
- Extracts configuration data from CUCM using AXL API
- Retrieves Phone, User, and Line configurations
- Saves data in JSON format
- Features progress tracking and error handling
- Output: `Phone.json`, `User.json`, `Line.json`

### 2. Data Transformation
- Converts JSON files to CSV format
- Extracts relevant fields for Webex migration
- Processes phone, user, and directory number data
- Output: `Phone.csv`, `User.csv`, `DirectoryNumber.csv`

### 3. Data Import
- Automates user and device import to Webex
- Uses Webex API for data push
- Generates detailed import summaries
- Supports both user and device imports
- Output: `import_summary.json`, `device_import_summary.json`

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `tqdm`
  - `os`
  - `json`
  - `csv`
  - `traceback`
- CUCM access with AXL API enabled
- Webex API access token with appropriate permissions

## Workflow

1. **Data Collection**:
   ```bash
   cd data_collection
   python cucm_export.py
   ```

2. **Data Transformation**:
   ```bash
   cd data_transformation
   python transformation.py
   ```

3. **Data Import**:
   ```bash
   cd data_import
   python webex_import.py
   python add_device.py
   ```

## Features

- End-to-end migration solution
- Progress tracking and error handling
- Detailed operation summaries
- Modular design for easy customization
- Support for bulk operations

## Directory Structure Details


sourcefolder/
├── data_collection/
│   ├── ConfigExports/
│   │   └── <siteCode>/
│   │       ├── Phone.json
│   │       ├── User.json
│   │       └── Line.json
│   └── README.md
├── data_transformation/
│   ├── output_csv/
│   │   ├── Phone.csv
│   │   ├── User.csv
│   │   └── DirectoryNumber.csv
│   └── README.md
├── data_import/
│   ├── import_summary.json
│   ├── device_import_summary.json
│   └── README.md
└── README.md


## Error Handling

- Each component includes robust error handling
- Failed operations are logged in summary files
- Process continues even if individual items fail
- Detailed error messages for troubleshooting

## Notes

- Ensure proper permissions for both CUCM and Webex
- Verify input file formats before processing
- Check summary files for operation results
- Back up data before running migration
- https://developer.webex.com/docs/authentication