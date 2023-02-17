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

def return_version_similarity(cpe,software_name,software_version):
    cpe_version = cpe[5]

    score = 0

    versions = [software_version]
    versions_in_name = re.findall(r"[0-9]+(?:\.[0-9]+)*",software_name) #checks if a version number is included in the name - often more accurate than what is stored on the registry
    versions.extend(versions_in_name)

    version_scores = []

    for version in versions: #calculates a version similarity score for both the version in the name (if there is one) and the actual listed software version
        current_score = 0

        cpe_version_split = cpe_version.replace("-",".").split(".") #replace function used to convert dates "2020-09-01" to a standard format using dots
        version_split = version.split(".")

        if len(cpe_version_split) > len(version_split): #iterates over the shorter of the versions and compares each of their fields, awarding a higher score for 
            for i,number in enumerate(version_split):   #having the same numbers at the start of the version, eg 1.2.3 is more similar to 1.3.4 than 2.2.3 is.
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

def return_importance_relationship_similarity(cpe,software_vendor,software_name,vendor_importance,name_importance):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

    software_vendor_split = software_vendor.split(" ")
    software_name_split = software_name.split(" ")

    importance_score = 0
    relationship_score = 0

    score_system = {"EQUAL":1,"SUBWORD":0.75,"SUBSTRING":0.15,"NONE":-0.5}
    other_fields_score_system = {"EQUAL":0.5,"SUBWORD":0.4,"SUBSTRING":0.1,"NONE":0}

    for field in cpe[6:]: #checks through all other fields in the cpe to see if any of them match any words in the software vendor or name.
        if field != "*":
            relationship_score += other_fields_score_system[return_relationship(software_vendor,field)]
            relationship_score += other_fields_score_system[return_relationship(software_name,field)]

    for word in cpe_vendor.replace("-","_").split("_"):
        #importance score 
        if word in software_vendor_split:
            importance_score += vendor_importance[software_vendor_split.index(word)]

        if word in software_name_split:
            importance_score += name_importance[software_name_split.index(word)]

        #vendor to vendor relationship
        relationship_score += score_system[return_relationship(software_vendor,word)]

        #name to vendor relationship
        relationship_score += score_system[return_relationship(software_name,word)] * 0.25

    for word in cpe_name.replace("-","_").split("_"): #checks if each word in the cpe name is in the software name or vendor
        #name to name relationship
        relationship_score += score_system[return_relationship(software_name,word)]

        #name to vendor relationship
        relationship_score += score_system[return_relationship(software_vendor,word)] * 0.25

    return importance_score,relationship_score

#*************************LEVENSHTEIN SCORE*************************

def return_levenshtein_similarity(cpe,software_vendor,software_name):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()

    score = 0

    #compare the levenshtein distance between the vendors and the names
    for c,s,multiplier in [[cpe_vendor,software_vendor,1],[cpe_name,software_name,1]]:
        max_string_len = max(len(c),len(s))
        score += Levenshtein.ratio(c,s) * multiplier

    return score

#*************************ENSEMBLE SCORE*************************

def ensemble_similarity(cpe,software_vendor,software_name,software_version,vendor_importance,name_importance):
    version_score = return_version_similarity(cpe,software_name,software_version)
    importance_score,relationship_score = return_importance_relationship_similarity(cpe,software_vendor,software_name,vendor_importance,name_importance)
    levenshtein_score = return_levenshtein_similarity(cpe,software_vendor,software_name)

    return 1 / (1 + math.exp(-sum([relationship_score,importance_score,levenshtein_score,version_score]) / 1.5))

#*************************IMPORTANCE ASSIGNING*************************

def assign_importance(string,important_words_list):
    formatted_string = string.lower().split()

    string_importance = []

    for word in formatted_string:
        if word in important_words_list: string_importance.append(1)
        else: string_importance.append(0.5)

    return string_importance