try:
    from ciscoaxl import axl
except:
    from data_collection.ciscoaxl import axl
import json
from collections import OrderedDict
from zeep.helpers import serialize_object
import datetime
import traceback
import multiprocessing as mp
from tqdm import tqdm
from sys import exit
import os
from pathlib import Path

ucmSourceContent = json.load(open("data_Collection/adapter/source.json"))
ucm_source = axl(
    username=ucmSourceContent["username"],
    password=ucmSourceContent["password"],
    cucm=ucmSourceContent["sourceCUCM"],
    cucm_version=ucmSourceContent["version"],
)


def cleanObject(data):
    # if 'locationName' in data and data['locationName']:
    #     print(data)
    #     exit()
    if 'vendorConfig' in data:
        del data['vendorConfig']
    if data != None:
        if type(data) != str:
            dictData = dict(serialize_object(data))
            returnedDict = dictData
            if "uuid" in dictData:
                del dictData["uuid"]
            for key, value in dictData.items():
                if key == "sigDigits":
                    continue
                if type(value) == str:
                    continue
                elif type(value) == OrderedDict:
                    if "_value_1" in value.keys():
                        returnedDict[key] = value["_value_1"]
                    else:
                        returnedDict[key] = cleanObject(value)
                elif type(value) == list:
                    tempdataList = []
                    for entries in value:
                        tempdataList.append(cleanObject(entries))
                    returnedDict[key] = tempdataList
            return returnedDict
        else:
            return data
    else:
        return data


def changeDeque(cleanedData):
    if isinstance(cleanedData, dict):
        if "_raw_elements" in cleanedData:
            configsDict = {
                entry.tag: entry.text
                for entry in cleanedData["_raw_elements"]
            }
            del cleanedData["_raw_elements"]
            configsDict.update(configsDict)

        if "_Element" in cleanedData:
            configsDict = {
                entry.tag: entry.text
                for entry in cleanedData["_Element"]
            }
            del cleanedData["_Element"]
            configsDict.update(configsDict)


        for key, val in cleanedData.items():
            if isinstance(val, dict):
                cleanedData[key] = changeDeque(val)

    elif isinstance(cleanedData, list) and isinstance(cleanedData[0], dict):
        for i in range(len(cleanedData)):
            cleanedData[i] = changeDeque(cleanedData[i])

    return cleanedData


def write_results(directory, data, dtype):
    try:
        if dtype in ["callpark", "directedcallpark"]:
            cleanedData = []
            for entry in data:
                uuid = None
                if "uuid" in entry:
                    uuid = entry["uuid"]
                tempCleanedData = cleanObject(entry)
                if uuid != None:
                    tempCleanedData["uuid"] = uuid
                cleanedData.append(tempCleanedData)
                del tempCleanedData
        else:
            cleanedData = [cleanObject(entry) for entry in data]
        if cleanedData:
            try:
                jsonString = json.dumps(
                    serialize_object(cleanedData), indent=4)
            except Exception as err:
                jsonString = []
                if "Object of type deque" in str(err):
                    #DO Something to remove the Deque
                    # print(cleanedData)
                    cleanedData = changeDeque(cleanedData)
                    jsonString = json.dumps(
                        serialize_object(cleanedData), indent=4)
                else:
                    # print(cleanedData)
                    print("Error Occured in writing " +
                          str(dtype) + " as json file: "+str(err))
                    traceback.print_exc()
            jsonFile = open(os.path.join(directory, dtype+".json"), "w")
            if isinstance(jsonString, list):
                for entry in jsonString:
                    jsonFile.write(entry)
            else:
                jsonFile.write(jsonString)
            print(f"Saved {dtype}.json")
            jsonFile.close()
        else:
            print(f"No Data found for-{dtype}")
    except Exception as err:
        # print(cleanedData)
        print("Error Occured in writing " +
              str(dtype) + " as json file: "+str(err))
        # print('Data::',data)
        traceback.print_exc()
    return True