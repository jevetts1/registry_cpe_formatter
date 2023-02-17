main_script.py:
Run to generate potential CPEs on your system.

cpe_similarity.py
Contains functions that return the similarity score between software information and a CPE.

registry_query.py
Contains a function that gathers information about software in the Uninstall registry.

cpe_dict_loader.py
Has functions that create a text file of NVDs CPEs, json of the CPEs, load the whole dataframe, and load the CPEs from text or json files.

matcher.py
Contains the function that iterates over the set of CPEs and returns a list of the best matches for a given set of software information.

utils.py
Quality of life utilities.

QUICK START
Run main_script.py