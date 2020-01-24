#!/usr/bin/env python

import os
import sys
import json
import time
import tarfile
import pandas as pd
from pathlib import Path
from flatten_json import flatten

def findKey(key, dictionary):
    for k, v in dictionary.iteritems():
        if k.lower().endswith(key.lower()):
            yield k
        elif isinstance(v, dict):
            for result in findKey(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in findKey(key, d):
                    yield result

def findValue(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in findValue(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in findValue(key, d):
                    yield result

def dict_sweep(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: dict_sweep(v, key) for k, v in input_dict.items() if k != key}

    elif isinstance(input_dict, list):
        return [dict_sweep(element, key) for element in input_dict]

    else:
        return input_dict

def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}        

configKeyList = ['sonusSipSigPort:sipSigPort', 'sonusIpPeer:ipPeer', 'sonusSipTrunkGroup:sipTrunkGroup', 'cac']

unwantedSubKeyList = ['name', 'ipaddress', 'prefix', 'prefixLength', 'policy', 'profile', 'preference', 'varianttype', 'method', 'ipAddressV6']

for filename in os.listdir('/root/cdb/'):
    os.system('pkill confd')
    os.system('pkill user-storage-trans-app')
    os.system('rm -f /opt/sonus/sbx/tailf/var/confd/cdb/*.cdb')
    os.system('rm -f /root/cdb/cfg.json')
    time.sleep(7)
    fileAbsPath = '/root/cdb/' + filename
    if os.path.exists(fileAbsPath):
        myTar = tarfile.open(fileAbsPath)
        myTar.extractall('/opt/sonus/sbx/tailf/var/confd/cdb/')
        myTar.close()
    print("HEYY 4")
    os.system('/opt/sonus/sbx/tailf/bin/confd -c /opt/sonus/sbx/tailf/confd.conf --foreground 2>&1 > /dev/null &')
    print("HEYY 3")
    time.sleep(5)
    print("HEYY 2")
    os.system('/root/user-storage-trans-app 2>&1 > /dev/null &')
    time.sleep(5)
    print("HEYY 1")
    os.system('echo "show configuration addressContext | nomore | display json" | /opt/sonus/sbx/tailf/bin/confd_cli -u admin > /root/cdb/cfg.json')

    print("HEYY")

    if os.path.exists('/root/cdb/cfg.json'):
        if os.stat('/root/cdb/cfg.json').st_size != 0:
           with open('/root/cdb/cfg.json', 'r') as f:
               data = json.loads(f.read())
           unwantedKeyList = []
           for unwantedSubKey in unwantedSubKeyList:
               unwantedKeyList.extend(list(findKey(unwantedSubKey, data)))
           
           for unwantedKey in unwantedKeyList:
               data = dict_sweep(data, unwantedKey)
           
           data = clean_empty(data)
           
           for configKey in configKeyList:
               if ':' in configKey:
                   csvFileName = configKey.split(':')[1] + '.csv'
               else:
                   csvFileName = configKey + '.csv'
           
           
               perConfigDataList = []
               perConfigDataList = findValue(configKey, data)
           
               if perConfigDataList != []:
                   for perConfigData in perConfigDataList:
                       if isinstance(perConfigData, list):
                           for config in perConfigData:
                               if os.path.exists(csvFileName):
                                   headerUse = False
                               else:
                                   headerUse = True
                               df = pd.DataFrame([flatten(config)])
                               df.to_csv(csvFileName, mode='a', index=False, encoding='utf-8', header=True)
                       elif isinstance(perConfigData, dict):
                           if os.path.exists(csvFileName):
                               headerUse = False
                           else:
                               headerUse = True
                           df = pd.DataFrame([flatten(perConfigData)])
                           df.to_csv(csvFileName, mode='a', index=False, encoding='utf-8', header=True)

for configKey in configKeyList:
    if ':' in configKey:
        csvFileName = configKey.split(':')[1] + '.csv'
    else:
        csvFileName = configKey + '.csv'

    rowValDictList = []

    consolidatedKeyList = []
    with open(csvFileName) as f:
        while True:
            line1 = f.readline().rstrip()
            line2 = f.readline().rstrip()
            if not line2: break  # EOF
            keyList = line1.split(',')
            valList = line2.split(',')
            rowValDict = {}
            for i in range(0,len(keyList)):
                rowValDict[keyList[i]] = valList[i]
            rowValDictList.append(rowValDict)
            consolidatedKeyList.extend(keyList)

    os.remove(csvFileName)

    consolidatedKeyList = list(set(consolidatedKeyList))
    
    with open(csvFileName, 'w') as f:
        f.write(','.join(consolidatedKeyList) + '\n')
    for rowValDict in rowValDictList:
        rowValList = []
        for consolidatedKey in consolidatedKeyList:
            if consolidatedKey in rowValDict:
                print("YAYY")
                rowValList.append(rowValDict[consolidatedKey])
            else:
                rowValList.append('')
        with open(csvFileName, 'a') as f:
            f.write(','.join(rowValList) + '\n')

for configKey in configKeyList:
    if ':' in configKey:
        csvFileName = configKey.split(':')[1] + '.csv'
    else:
        csvFileName = configKey + '.csv'

    replaceStringDict = {
         "a-only": "1",
         "a-srv-naptr" : "2",
         "allow": "1",
         "both": "1",
         "convert": "0",
         "default": "0",
         "disabled": "0",
         "dryUp": "1",
         "enabled": "1",
         "exclude": "0",
         "lastProvResponse": "1",
         "localignored": "0",
         "noAction": "0",
         "none": "0",
         "outOfService": "0",
         "passthru": "1",
         "required": "1",
         "supported": "1",
         "synchronous": "0",
         "treatAsFaxTransmissionIndication": "1",
         "unlimited": "100",
         "inService": "1",
         "passive": "0",
         "matchSigAddrType": "0",
         "firstProvResponse": "2",
         "force": "1",
         "challengeForRegister": "1",
         "unlimited": "100",
         "noValidation": "0",
         "release": "1"
    }

    with open(csvFileName, "r") as fin:
        with open(csvFileName + '_1', "w") as fout:
            for line in fin:
                for key, val in replaceStringDict.items():
                    line = line.replace(key, val)
                fout.write(line)
