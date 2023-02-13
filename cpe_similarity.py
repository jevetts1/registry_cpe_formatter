import math,re
from string_matching import match_string

def return_relationship(string_super,string_sub):
    if string_sub == string_super:
        return "EQUAL"
    
    for word in string_super.split():
        if string_sub == word:
            return "SUBWORD"

    if string_sub in string_super:
        return "SUBSTRING"

    return "NONE"
        

def return_similarity(cpe,software_vendor,software_name):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

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

    return 1 / (1 + math.exp(-score)) #return a value between 0 and 1

def return_version_similarity(cpe,software_name,software_version):
    cpe_version = cpe[5]

    score = 0

    versions = [software_version]

    version_in_name = re.search(r"([0-9]+.)+[0-9]+",software_name) #checks if a version number is included in the name - often more accurate than what is stored on the registry

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

        current_score -= abs(len(version_split) - len(cpe_version_split)) * 0.5
        
        version_scores.append(current_score)
    
    score += max(version_scores) 

    if cpe_version == "-":
        score -= 1

    return 1 / (1 + math.exp(-score)) #return a value between 0 and 1

if __name__ == "__main__":
    print(return_similarity("cpe:2.3:a:python:python:3.9.7","Python Software Foundation","Python 3.9.7 (x64)","1.0.0.9"))
    print(return_similarity("cpe:/a:python:python:3.9.7","Python Software Foundation","Python","3.7.7"))