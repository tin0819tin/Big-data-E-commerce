#SSHTunnelForwarder(ssh)
import pandas as pd
import numpy as np
import os
import re
from sshtunnel import SSHTunnelForwarder
import pymongo


#Connecting to MongoDB
MONGO_HOST = "3.92.176.18"
MONGO_USER = "ubuntu"
MONGO_DB = "TTRI"
# MONGO_COLLECTION = "COLLECTION_NAME"
# define ssh tunnel
server = SSHTunnelForwarder(
MONGO_HOST,
ssh_username=MONGO_USER,
ssh_pkey="/Users/apple/Desktop/Bigdata & E-commerce/EC_ec2-key.pem.txt",
remote_bind_address=('127.0.0.1', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
collection_names = client['TTRI'].list_collection_names()

#Collecting Data
dict_keys = ['_id', 'Name', 'ReviewCount', 'Rating', 'Price', 'Url', 'ModifiedDate', 'FullMaterial', 'CreateDate', 'Bullets', 'Brand', 'Gender', 'ImageUrl', 'Description', 'Material', 'Sport', 'Feature', 'Clothing', 'StyelNumber', 'Fulltext']
pd_dict = {}

#Create column list
for i in dict_keys:
    pd_dict[i] = []

'''
print(pd_dict)
x = client['TTRI']['Products'].find_one()
for i,value in enumerate(dict_keys):
    #print(i,value)
    print("{} : {} -- ({})".format(value, x[value], type(x[value])))
'''

print("Collecting Data")
num = 0
for i in client['TTRI']['Products'].find():
    #Adding item
    for index in i:
        if index in dict_keys:
            pd_dict[index].append(i[index])
        else:
            #Adding new columns
            dict_keys.append(index)
            #Make new columns for all previous items
            pd_dict[index] = []
            for j in range(num):
                pd_dict[index].append(None)
            pd_dict[index].append(i[index])

    #Check every columns has same length
    for check in pd_dict:
        if(len(pd_dict[check]) < num+1):
            pd_dict[check].append(None)

    #Count item       
    num += 1

#Debug
'''
print(num)
print(dict_keys)
for i in pd_dict:
    print("{} : length = {}".format(i, len(pd_dict[i])))
'''

#Create dataframe
print("Creating Dataframe")
df = pd.DataFrame(pd_dict)

output_path_csv = 'MongoDB.csv'
output_path_excel = 'MongoDB.xlsx'

print("Loading csv")
df.to_csv(output_path_csv)
print("Loading excel")
df.to_excel(output_path_excel)

print("Collecting Data complete!")
client.close()