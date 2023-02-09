import math,re

def is_subset(string_super,string_sub):
    if string_sub in string_super:return True
    else: return False

def is_subword(string_super,string_sub):
    for word in string_super.split():
        if string_sub == word:
            return True
    
    return False

def return_similarity(cpe,software_vendor,software_name,software_version):
    cpe_vendor = cpe.split(":")[2]
    cpe_name = cpe.split(":")[3]
    cpe_version = cpe.split(":")[4]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()
    software_version = software_version.lower()

    score = 0

    for word in cpe_vendor.split("_"):
        #vendor to vendor relationship
        if is_subword(software_vendor,word):
            score += 1

        elif is_subset(software_vendor,word):
            score += 0.25

        else:
            score -= 0.5

        #name to vendor relationship
        if is_subword(software_name,word):
            score += 1

        elif is_subset(software_name,word):
            score += 0.25

        else:
            score -= 0.1

    for word in cpe_name.split("_"):
        #name to name relationship
        if is_subword(software_name,word):
            score += 1

        elif is_subset(software_name,word):
            score += 0.25

        else:
            score -= 0.5

        #vendor to name relationship
        if is_subword(software_vendor,word):
            score += 1

        elif is_subset(software_vendor,word):
            score += 0.25

        else:
            score -= 0.1

    versions = [software_version]

    version_in_name = re.search(r"([0-9]+.)+[0-9]+",software_name)

    if version_in_name:
        version_in_name = software_name[version_in_name.span()[0]:version_in_name.span()[1]]
        versions.append(version_in_name)

    version_scores = []

    for version in versions:
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

        score -= abs(len(version_split) - len(cpe_version_split)) * 0.5
        
        version_scores.append(current_score)
    
    score += max(version_scores)

    return 1 / (1 + math.exp(-score))

if __name__ == "__main__":
    print(return_similarity("cpe:/a:python:python:3.9.7","Python Software Foundation","Python 3.9.7 (x64)","1.0.0.9"))
    print(return_similarity("cpe:/a:python:python:3.9.7","Python Software Foundation","Python (x64)","1.0.0.9"))