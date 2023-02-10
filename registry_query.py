import winreg

def get_installed_software(): #returns a list of dictionaries of {Vendor:vendor,Name:name,Version:version}
    software_list = []
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") #software information is easy to access in the Uninstall registry key

    for i in range(winreg.QueryInfoKey(key)[0]): #iterates through all subkeys (software) then appends a dictionary to the list with the information inside
        software = {}

        subkey = winreg.EnumKey(key, i)
        subkey_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" + "\\" + subkey
        subkey_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
        
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
            pass

        software_list.append(software)

    return software_list

if __name__ == "__main__":
    software = get_installed_software()
    for s in software:
        print(s)
