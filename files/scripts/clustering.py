from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import AffinityPropagation
from collections import OrderedDict, defaultdict
import numpy
import scipy.stats as stats
import pandas as pd
import os.path
import csv
import json

# clustering algorithm
def cluster_fun(file_path):
    df = pd.read_csv (file_path)
    X = df.iloc[:,:]
    af = AffinityPropagation(preference=-50)
    af.fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    cluster = defaultdict(list)
    for index in range(len(labels)):
        cluster[str(labels[index])].append(str(index))
    return cluster

#check if file exists in the given path then pass one by one file to the clustering algorithm
def main():
    #read the the configuration
    conf_list = [sipSigPort,ipPeer,sipTrunkGroup,cac]
    for i in conf_list:
        input_path = os.path.join('C:\\Users\\sbalakatti\\Desktop\\Technothon', i+".csv")
        output_path = os.path.join('C:\\Users\\sbalakatti\\Desktop\\Technothon', i+".json")
        if os.path.exists(input_path):
            cluster=cluster_fun(input_path)  
            cluster=dict(cluster)
            json_data=json.dumps(cluster)
            with open(output_path,'a') as file:
                file.write(json_data)
        return cluster
cluster = main()
