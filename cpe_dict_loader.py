import pandas as pd
import os

def create_cpe_txt(): #creates a text file in the current directory populated with cpes from NVD separated by new lines
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url, xpath=".//doc:cpe-item", namespaces={'doc': 'http://cpe.mitre.org/dictionary/2.0'})

    cpes = df.name.to_list()

    with open("NVD_cpes.txt","w") as file:
        for line in cpes:
            file.write(line + "\n")
        file.close()

    return os.path.dirname(os.path.abspath(__file__)) + "\\NVD_cpes.txt"

def load_dict_dataframe(): #returns the entire NVD dictionary dataframe
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url, xpath=".//doc:cpe-item", namespaces={'doc': 'http://cpe.mitre.org/dictionary/2.0'})

    return df

def load_cpe_txt(): #loads the cpe file in the current directory
    with open("NVD_cpes.txt","r") as file:
        cpes = file.readlines()
        file.close()

    return cpes