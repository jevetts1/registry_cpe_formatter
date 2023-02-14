main.ipynb:
Run all the cells to generate potential CPEs on your system.

cpe_similarity.py
Contains functions that return the similarity score between software information and a CPE.

registry_query.py
Contains a function that gathers information about software in the Uninstall registry.

cpe_dict_loader.py
Has functions that create a text file of NVDs CPEs, json of the CPEs, load the whole dataframe, and load the CPEs from text or json files.

QUICK START
Run `create_processed_cpe_json()` to create the json file.
Run the vendor_ml.ipynb script to train a model and then save it.
On the main script, run the imports, software inventory and cpe_list cells and then the matches cell.