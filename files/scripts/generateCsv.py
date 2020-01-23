#!/usr/bin/env python
import json
import pandas as pd
from pathlib import Path
from flatten_json import flatten

def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k.lower().endswith(key.lower()):
            yield k
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


def dict_sweep(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: dict_sweep(v, key) for k, v in input_dict.items() if k != key}

    elif isinstance(input_dict, list):
        return [dict_sweep(element, key) for element in input_dict]

    else:
        return input_dict

p = Path(r'config_1.json')
with p.open('r', encoding='utf-8') as f:
    data = json.loads(f.read())

unwantedSubKeyList = ['name', 'ipaddress', 'prefix']

unwantedKeyList = []

for unwantedSubKey in unwantedSubKeyList:
    unwantedKeyList.extend(list(find(unwantedSubKey, data)))

for unwantedKey in unwantedKeyList:
    data = dict_sweep(data, unwantedKey)

df = pd.DataFrame([flatten(data)])
df.to_csv('test1.csv', index=False, encoding='utf-8')
