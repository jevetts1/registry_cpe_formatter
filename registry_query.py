import winreg

def get_installed_software(): #returns a list of dictionaries of {Vendor:vendor,Name:name,Version:version}
    _32bit_software_key = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall" 
    _64bit_software_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    software_list = []

    for software_key in [_32bit_software_key,_64bit_software_key]:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,software_key) #software information is easy to access in the Uninstall registry key

        for i in range(winreg.QueryInfoKey(key)[0]): #iterates through all subkeys (software) then appends a dictionary to the list with the information inside
            software = {}

            subkey = winreg.EnumKey(key, i)
            subkey_path = software_key + "\\" + subkey
            subkey_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,subkey_path)
            
            try:
                software["Vendor"] = winreg.QueryValueEx(subkey_handle, "Publisher")[0]
            except:
                pass
            try:
                software["Name"] = winreg.QueryValueEx(subkey_handle, "DisplayName")[0]
            except:
                pass
            try:
                software["Version"] = winreg.QueryValueEx(subkey_handle, "DisplayVersion")[0]
            except:
                software["Version"] = ""

            software_list.append(software)

    return software_list

if __name__ == "__main__":
    software = get_installed_software()
    for s in software:
        print(s)
