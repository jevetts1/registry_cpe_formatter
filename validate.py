def validate_selected_cpe(cpe,software_vendor,software_name,software_version):
    cpe_vendor = cpe[3]
    cpe_name = cpe[4]
    cpe_version = cpe[5]

    software_vendor = software_vendor.lower()
    software_name = software_name.lower()
    software_version = software_version.lower()

    validation = {"Vendor":False,"Name":False,"Version":False}

    if cpe_vendor in software_vendor:
        validation["Vendor"] = True

    if cpe_name in software_name:
        validation["Name"] = True

    if cpe_version in software_version:
        validation["Version"] = True

    return validation