import math

def importance(string): #potentially useful
    importance = []

    for word in string.split():
        if word[0].upper() == word[0]:
            pass

def string_similarity(cpe_string,searched_string):
    score = 0

    cpe_string = cpe_string.lower()
    searched_string = searched_string.lower()

    if cpe_string == searched_string:
        return 1

    elif cpe_string in searched_string:
        score += 2

        score -= len(searched_string.replace(cpe_string,"")) * 0.01

    elif searched_string in cpe_string:
        score += 2

        score -= len(cpe_string.replace(searched_string,"")) * 0.01

    else:
        for word in cpe_string.split():
            if word in searched_string:
                score += 0.25
            
            else:
                score -= 0.1

        for word in searched_string.split():
            if word in cpe_string:
                score += 0.25
            
            else:
                score -= 0.1

    return 1 / (1 + math.exp(-score))

def version_similarity(cpe_version,version):
    cpe_version_list = cpe_version.split(".")
    version_list = version.split(".")

    score = 0

    if cpe_version == version:
        return 1

    elif cpe_version in version:
        score += 2

        score -= len(version.replace(cpe_version,"")) * 0.01

    elif version in cpe_version:
        score += 2

        score -= len(cpe_version.replace(version,"")) * 0.01

    if len(cpe_version_list) < len(version_list):
        for i,number in enumerate(cpe_version_list):
            if number == version_list[i]:
                score += 1 * math.exp(-i * 0.5)

            else:
                score -= 1 * math.exp(-i * 0.5)

    else:
        for i,number in enumerate(version_list):
            if number == cpe_version_list[i]:
                score += 1 * math.exp(-i * 0.5)

            else:
                score -= 1 * math.exp(-i * 0.5)

    return 1 / (1 + math.exp(-score))