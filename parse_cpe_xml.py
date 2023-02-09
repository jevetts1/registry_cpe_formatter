import pandas as pd

def return_cpe_df():
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip"
    df = pd.read_xml(url, xpath=".//doc:cpe-item", namespaces={'doc': 'http://cpe.mitre.org/dictionary/2.0'})

    return df