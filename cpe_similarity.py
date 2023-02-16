import math,re,Levenshtein
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

#*************************STRING RELATIONSHIP SCORE*************************

def return_relationship_similarity(cpe,software_vendor,software_name,software_version):
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

    versions_in_name = re.findall(r"[0-9]+(?:\.[0-9]+)*",software_name) #checks if a version number is included in the name - often more accurate than what is stored on the registry

    versions.extend(versions_in_name)

    version_scores = []

    for version in versions: #calculates a version similarity score for both the version in the name (if there is one) and the actual listed software version
        current_score = 0

        cpe_version_split = cpe_version.replace("-",".").split(".") #replace function used to convert dates "2020-09-01" to a standard format using dots
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

#*************************IMPORTANCE VECTOR SCORE*************************

def return_importance_weighted_similarity(cpe,software_vendor,software_name,vendor_importance,name_importance):
    cpe_vendor = cpe[3]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

    score = 0

    software_vendor_split = software_vendor.split(" ")
    software_name_split = software_name.split(" ")

    for word in cpe_vendor.replace("-","_").split("_"):
        if word in software_vendor_split:
            score += vendor_importance[software_vendor_split.index(word)]

        if word in software_name_split:
            score += name_importance[software_name_split.index(word)]

    return score

#*************************LEVENSHTEIN SCORE*************************

def return_levenshtein_similarity(cpe,software_vendor,software_name):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]
    cpe_version = cpe[5]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

    score = 0

    for c,s,multiplier in [[cpe_vendor,software_vendor,1],[cpe_name,software_name,1]]:
        max_string_len = max(len(c),len(s))
        score += Levenshtein.ratio(c,s) * multiplier

    return score

#*************************ENSEMBLE SCORE*************************

def ensemble_similarity(cpe,software_vendor,software_name,software_version,vendor_importance,name_importance):
    relationship_score = return_relationship_similarity(cpe,software_vendor,software_name,software_version)
    importance_score = return_importance_weighted_similarity(cpe,software_vendor,software_name,vendor_importance,name_importance)
    levenshtein_score = return_levenshtein_similarity(cpe,software_vendor,software_name)

    return 1 / (1 + math.exp(-sum([relationship_score,importance_score,levenshtein_score]) / 2))

#*************************IMPORTANCE ASSIGNING*************************

def assign_importance(string,important_words_list):
    formatted_string = string.lower().split()

    string_importance = []

    for word in formatted_string:
        if word in important_words_list: string_importance.append(1)
        else: string_importance.append(0.5)

    return string_importance

if __name__ == "__main__":
    print(ensemble_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:*:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Java","0.02",[1,0.2],[0.4,0.6,0.1,1]))
    print(ensemble_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:java:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Java","0.0.2",[1,0.2],[0.4,0.6,0.1,1]))
    print(ensemble_similarity("cpe:2.3:a:microsoft:visual_studio_code:0.0.2:*:*:*:*:java:*:*".split(":"),"Microsoft Corporation","Visual Studio Code Python","0.0.2",[1,0.2],[0.4,0.6,0.1,1]))