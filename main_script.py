from cpe_dict_loader import *
from registry_query import *
from cpe_similarity import *
from matcher import *
import json,random

#***************************only run first time***************************
print("Generating vendors list..." + " " * 20,end = "\r")
create_cpe_vendor_list()

print("Generating processed CPEs JSON..." + " " * 20,end = "\r")
create_processed_cpe_json()

#*************************************************************************

print("Generating software inventory..." + " " * 20,end = "\r")
software_inventory = get_installed_software()

print("Loading CPE list..." + " " * 20,end = "\r")
cpe_list = load_cpe_processed_json()

print("Opening test set..." + " " * 20,end = "\r")
with open("test_cpe_set.json","r") as file:
    test_set = json.load(file)
    file.close()

print("Opening vendor list..." + " " * 20,end = "\r")
with open("NVD_vendors.txt","r") as file:
    vendors_list = file.read().splitlines()
    file.close()

matches = match_software(cpe_list,software_inventory,vendors_list)
matches = sorted(matches,key = lambda x:x["Best_match"]["Similarity"])

print(matches)