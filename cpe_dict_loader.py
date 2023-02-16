import pandas as pd
import os,json,re

def create_cpe_txt(): #creates a text file in the current directory populated with cpes from NVD separated by new lines
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url,xpath=".//doc:cpe23-item",namespaces={'doc':"http://scap.nist.gov/schema/cpe-extension/2.3"})

    cpes = df.name.to_list()

    with open("NVD_cpes.txt","w") as file:
        for line in cpes:
            file.write(line + "\n")
        file.close()

    return os.path.dirname(os.path.abspath(__file__)) + "\\NVD_cpes.txt"

def create_cpe_vendor_list():
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url,xpath=".//doc:cpe23-item",namespaces={'doc':"http://scap.nist.gov/schema/cpe-extension/2.3"})

    cpes = df.name.to_list()

    with open("NVD_vendors.txt","w") as file:
        for i,line in enumerate(cpes):
            if i > 0:
                if cpes[i - 1].split(":")[3] != line.split(":")[3]:
                    file.write(line.split(":")[3] + "\n")

            else:
                file.write(line.split(":")[3] + "\n")

        file.close()

    return os.path.dirname(os.path.abspath(__file__)) + "\\NVD_vendors.txt"

def load_dict_dataframe(): #returns the entire NVD dictionary dataframe
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url,xpath=".//doc:cpe23-item",namespaces={'doc':"http://scap.nist.gov/schema/cpe-extension/2.3"})

    return df

def load_cpe_txt(): #loads the cpe file in the current directory
    with open("NVD_cpes.txt","r") as file:
        cpes = file.read().splitlines()
        file.close()

    return cpes

def load_cpe_processed_json():
    with open("NVD_cpes_processed.json","r") as file:
        json_file = json.load(file)
        file.close()

    return json_file

def create_processed_cpe_json():
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url,xpath=".//doc:cpe23-item",namespaces={'doc':"http://scap.nist.gov/schema/cpe-extension/2.3"})

    cpes = df.name.to_list()

    cpe_array = []

    for cpe in cpes:
        split_cpe = re.split(r'(?<=[^\\]):+',cpe)

        for i,field in enumerate(split_cpe):
            split_cpe[i] = field.replace("\\","")

        cpe_array.append([cpe,split_cpe])

    with open("NVD_cpes_processed.json","w") as file:
        json.dump(cpe_array,file)
        file.close()

    return os.path.dirname(os.path.abspath(__file__)) + "\\NVD_cpes_processed.json"

if __name__ == "__main__":
    create_processed_cpe_json()