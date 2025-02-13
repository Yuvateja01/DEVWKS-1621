# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 14:18:34 2021

@author: ashimis3
"""

import sys
import time
import os
import json
import traceback
from tqdm import tqdm
from adapter.appcore import *

sys.path.append("../")

def create_directory(directory):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory (str): Path of the directory to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_cucm_connectivity(ucm_source):
    """
    Check CUCM connectivity.
    
    Args:
        ucm_source: CUCM source object.
        
    Returns:
        bool: True if connectivity is successful, False otherwise.
    """
    if not ucm_source.check_cucm():
        print("CUCM AXL Connectivity issue: \n\t1. Check Credentials\n\t2. Check AXL Connectivity\n\t3. Check Account locked status.")
        return False
    return True

def pull_phones(ucm_source, configList):
    """
    Pull phones using listPhone and getPhone methods.
    
    Args:
        ucm_source: CUCM source object.
        configList (dict): Configuration list for different entities.
        
    Returns:
        list: List of phone configurations.
    """
    start = time.time()
    listPhones = ucm_source.client.listPhone(configList["Phone"][0], returnedTags=configList["Phone"][1])
    if listPhones and listPhones["return"]:
        phones = listPhones["return"]["phone"]
    else:
        print("\nNo Phones found.")
        phones = []
    phones = [cleanObject(phone) for phone in phones]

    phone_configs = []
    for phone in tqdm(phones, desc="Fetching full phone configurations"):
        try:
            phone_resp = ucm_source.client.getPhone(name=phone["name"])
            if phone_resp and phone_resp["return"]:
                phone_configs.append(phone_resp["return"]["phone"])
        except Exception as e:
            print(f"Error fetching phone {phone['name']}: {str(e)}")

    end = time.time()
    print(f"\nFound {len(phone_configs)} Phones in {round(end - start, 2)} seconds. Processing...")
    return phone_configs

def pull_users(ucm_source, phone_configs, directory):
    """
    Extract ownerUserName from phone configurations and pull users using getUser.
    
    Args:
        ucm_source: CUCM source object.
        phone_configs (list): List of phone configurations.
        directory (str): Directory to save the results.
        
    Returns:
        list: List of user configurations.
    """
    phone_configs = json.loads(open(f"{directory}/Phone.json").read())
    owner_usernames = set(phone_data.get("ownerUserName") for phone_data in phone_configs if phone_data.get("ownerUserName"))
    print(f"\nFound {len(owner_usernames)} unique ownerUserNames. Pulling Users...")

    users = []
    for username in tqdm(owner_usernames, desc="Fetching user configurations"):
        try:
            user_resp = ucm_source.client.getUser(userid=username)
            if user_resp and user_resp["return"]:
                users.append(user_resp["return"]["user"])
        except Exception as e:
            print(f"Error pulling user {username}: {str(e)}")
    return users

def pull_lines(ucm_source, phone_configs):
    """
    Extract unique line + partition combinations from phone configurations and pull lines using getLine.
    
    Args:
        ucm_source: CUCM source object.
        phone_configs (list): List of phone configurations.
        
    Returns:
        list: List of line configurations.
    """
    line_partition_combinations = set()
    for phone in phone_configs:
        lines = []
        if phone.get("lines"):
            lines = phone["lines"].get("line", [])
        for line in lines:
            pattern = line.get("dirn", {}).get("pattern")
            partition = line.get("dirn", {}).get("routePartitionName")
            if pattern and partition:
                line_partition_combinations.add((pattern, partition))

    print(f"\nFound {len(line_partition_combinations)} unique line + partition combinations. Pulling Lines...")

    lines = []
    for pattern, partition in tqdm(line_partition_combinations, desc="Fetching line configurations"):
        try:
            line_resp = ucm_source.client.getLine(pattern=pattern, routePartitionName=partition)
            if line_resp and line_resp["return"]:
                lines.append(line_resp["return"]["line"])
        except Exception as e:
            print(f"Error pulling line {pattern} in partition {partition}: {str(e)}")
    return lines

def main():
    """
    Main function to execute the data collection process.
    """
    try:
        # Get site code from the source content
        siteCode = ucmSourceContent["siteCode"]

        # Define directory for saving configuration exports
        directory = f"ConfigExports/{siteCode}"

        # Create directory if it doesn't exist
        create_directory(directory)

        # Check CUCM connectivity
        if not check_cucm_connectivity(ucm_source):
            exit()

        # Define configuration list for different entities
        configList = {
            "Phone": [{"devicePoolName": "Test_DP"}, {"name": ""}, "phone"],
            "User": [{"userid": "ad"}, {"userid": "", "firstName": "", "lastName": ""}, "user"],
            "Line": [{"pattern": "1111"}, {"pattern": ""}, "line"],
        }

        # Step 1: Pull Phones using list and get methods
        phone_configs = pull_phones(ucm_source, configList)
        write_results(directory, phone_configs, "Phone")

        # Step 2: Extract ownerUserName and pull Users
        phone_configs_dict = json.loads(open(f"{directory}/Phone.json").read())
        users = pull_users(ucm_source, phone_configs_dict, directory)
        write_results(directory, users, "User")

        # Step 3: Extract unique line + partition combinations and pull Lines
        lines = pull_lines(ucm_source, phone_configs_dict)
        write_results(directory, lines, "Line")

        print("\nData extraction completed successfully.")

    except Exception as e:
        print("Error Occurred:", str(e))
        traceback.print_exc()

if __name__ == "__main__":
    main()
