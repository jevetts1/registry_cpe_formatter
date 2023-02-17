import pandas as pd
import os,json,re

def load_dict_dataframe(): #returns the entire NVD dictionary dataframe
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url,xpath=".//doc:cpe23-item",namespaces={'doc':"http://scap.nist.gov/schema/cpe-extension/2.3"})

    return df

def create_cpe_vendor_list(): #creates a list of only CPE vendors
    df = load_dict_dataframe()

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

def load_cpe_processed_json(): #loads the CPE json in the current directory
    with open("NVD_cpes_processed.json","r") as file:
        json_file = json.load(file)
        file.close()

    return json_file

def create_processed_cpe_json(): #create a CPE json in the current directory, where each entry in the list
    df = load_dict_dataframe()   #is another list of [cpe,split_cpe] where split cpe is a cpe split into all of its fields separately.

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