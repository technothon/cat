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

unwantedSubKeyList = ['name', 'ipaddress', 'prefix', 'prefixLength', 'policy']

for filename in os.listdir('/root/cdb/'):
    fileAbsPath = '/root/cdb/' + filename
    myTar = tarfile.open(fileAbsPath)
    myTar.extractall('/opt/sonus/sbx/tailf/var/confd/cdb/')
    myTar.close()
    os.system('/opt/sonus/sbx/tailf/bin/confd -c /opt/sonus/sbx/tailf/confd.conf --foreground 2>&1 > /dev/null &')
    time.sleep(5)
    os.system('/root/user-storage-trans-app 2>&1 > /dev/null &')
    time.sleep(2)
    os.system('echo "show configuration addressContext | nomore | display json" | /opt/sonus/sbx/tailf/bin/confd_cli -u admin > /root/cdb/cfg.json')
    with open(sys.argv[1], 'r') as f:
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
                        df.to_csv(csvFileName, mode='a', index=False, encoding='utf-8', header=headerUse)
                elif isinstance(perConfigData, dict):
                    if os.path.exists(csvFileName):
                        headerUse = False
                    else:
                        headerUse = True
                    df = pd.DataFrame([flatten(perConfigData)])
                    df.to_csv(csvFileName, mode='a', index=False, encoding='utf-8', header=headerUse)
