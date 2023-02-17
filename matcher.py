from cpe_similarity import *
from utils import *
from IPython.display import clear_output

def match_software(cpe_list,software_list,vendors_list,platforms = ["windows"],verbose = True):
    all_matches = []

    print("Starting matching...")

    for i,software in enumerate(software_list):
        if verbose: print(progress_bar(i / len(software_list)),f"{round(i / len(software_list) * 100,2)}% of software matched.")

        best_match = {"CPE":None,"Similarity":0}

        if software.get("Vendor") and software.get("Name"):  
            vendor_importance = assign_importance(software.get("Vendor"),vendors_list)
            name_importance = assign_importance(software.get("Name"),vendors_list)
            
        else:
            continue

        for j,cpe in enumerate(cpe_list):  
            if verbose and j % 1000 == 0: print(progress_bar(j / len(cpe_list)),f"{round(j / len(cpe_list) * 100,1)}% of CPEs checked for current software.",end = "\r")

            score = ensemble_similarity(cpe[1],software.get("Vendor"),software.get("Name"),software.get("Version"),vendor_importance,name_importance)

            if score > best_match["Similarity"] and cpe[1][2] == "a" and cpe[1][10] in platforms + ["*"]:
                best_match["CPE"] = cpe[0]
                best_match["Similarity"] = score

        all_matches.append({"Software":software,"Best_match":best_match})   
        
        if verbose:
            print(" " * 100,end = "\r")
            print("\33[1A\33[1A") #moves cursor up two lines

    return all_matches