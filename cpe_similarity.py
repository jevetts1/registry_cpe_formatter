import math,re
import numpy as np

def return_relationship(string_super,string_sub):
    if string_sub == string_super:
        return "EQUAL"
    
    for word in string_super.lower().replace("_"," ").replace("-"," ").split(" "):
        if string_sub == word:
            return "SUBWORD"

        if word in string_sub:
            return "SUBSTRING"

    if string_sub in string_super:
        return "SUBSTRING"

    return "NONE"

def return_similarity(cpe,software_vendor,software_name,software_version):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]
    cpe_version = cpe[5]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()
    software_version = software_version.lower()

    score = 0

    score_system = {"EQUAL":1,"SUBWORD":0.75,"SUBSTRING":0.15,"NONE":-0.5}

    for word in cpe_vendor.replace("-","_").split("_"): #checks if each word in the cpe vendor is in the software name or vendor
        #vendor to vendor relationship
        score += score_system[return_relationship(software_vendor,word)]

        #name to vendor relationship
        score += score_system[return_relationship(software_name,word)] * 0.25

    for word in cpe_name.replace("-","_").split("_"): #checks if each word in the cpe name is in the software name or vendor
        #name to name relationship
        score += score_system[return_relationship(software_name,word)]

        #name to vendor relationship
        score += score_system[return_relationship(software_vendor,word)] * 0.25

    other_fields_score_system = {"EQUAL":0.5,"SUBWORD":0.4,"SUBSTRING":0.1,"NONE":0}

    for field in cpe[6:]:
        if field != "*":
            score += other_fields_score_system[return_relationship(software_vendor,field)]
            score += other_fields_score_system[return_relationship(software_name,field)]

    versions = [software_version]

    version_in_name = re.search(r"([0-9]+\.)+[0-9]+",software_name) #checks if a version number is included in the name - often more accurate than what is stored on the registry

    if version_in_name:
        version_in_name = software_name[version_in_name.span()[0]:version_in_name.span()[1]]
        versions.append(version_in_name)

    version_scores = []

    for version in versions: #calculates a version similarity score for both the version in the name (if there is one) and the actual listed software version
        current_score = 0

        cpe_version_split = cpe_version.split(".")
        version_split = version.split(".")

        if len(cpe_version_split) > len(version_split):
            for i,number in enumerate(version_split):
                if number == cpe_version_split[i]:
                    current_score += 0.5 / (i + 1)

                else:
                    current_score -= 0.5 / (i + 1)

        else:
            for i,number in enumerate(cpe_version_split):
                if number == version_split[i]:
                    current_score += 0.5 / (i + 1)

                else:
                    current_score -= 0.5 / (i + 1)

        current_score -= abs(len(version_split) - len(cpe_version_split)) * 0.5 #subtracts from the score if the versions are of different lengths
        
        version_scores.append(current_score)
    
    score += max(version_scores) 

    return score

def return_importance_weighted_similarity(cpe,software_vendor,software_name,vendor_importance,name_importance):
    cpe_vendor = cpe[3]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

    score = 0

    software_vendor_split = software_vendor.replace("_"," ").replace("-"," ").split(" ")
    software_name_split = software_name.replace("_"," ").replace("-"," ").split(" ")

    vendor_importance_weighted = [0 for x in range(len(software_vendor_split))]
    name_importance_weighted = [0 for x in range(len(software_name_split))]

    for i,word in enumerate(software_vendor_split):
        if word in cpe_vendor:
            score += vendor_importance[i]
        
        else:
            score -= vendor_importance[i] * 0.5

    for i,word in enumerate(software_name_split):
        if word in cpe_vendor:
            score += name_importance[i] * 0.5

        else:
            score -= name_importance[i] * 0.25

    return score

if __name__ == "__main__":
    print(return_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:*:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Java","0.02"))
    print(return_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:java:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Java Edition","0.02"))
    print(return_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:java:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Python Edition","0.02"))