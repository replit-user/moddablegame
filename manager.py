import json
import os
import sys

def mod_exists(save_data, name, version, path, header):
    for mod in save_data["mods"]:
        if (
            mod.get("name") == name and
            mod.get("version") == version and
            mod.get("path") == path and
            mod.get("header") == header
        ):
            return True
    return False

def mod(selection):
    with open("./mods.json", "r") as f:
        mods = json.load(f)
    if __name__ == "__main__":
        print("\n=== MOD MANAGER ===")
        for i, mod in enumerate(mods["mods"]):
            status = "ON" if mod.get("enabled") else "OFF"
            print(f"{i+1}. {mod['name']} [{status}]")

    try:

        if selection == "d":
            mods_path = os.path.join(os.path.dirname(__file__), "mods")
            with open("mods.json", "r") as f:
                save_data = json.load(f)
            with open("mods.json","w") as f:
                f.write("")
            for entry in os.listdir(mods_path):
                full_path = os.path.join(mods_path, entry)
                if os.path.isdir(full_path):
                    manifest_path = os.path.join(full_path, "manifest.json")
                    if os.path.isfile(manifest_path):
                        with open(manifest_path, "r") as mf:
                            data = json.load(mf)

                        name = data.get("name")
                        version = data.get("version")
                        init = data.get("ready")  # presumably some mod path or flag
                        main = data.get("main")
                        # Use manifest_path for header
                        header = f"./mods/{entry}/manifest.json"
                        # Use init as path if it represents mod's path
                        path = init  

                        if name and version and init and main:
                            if not mod_exists(save_data, name, version, path, header):
                                save_data["mods"].append({
                                    "name": name,
                                    "version": version,
                                    "enabled": True,  # or False as needed
                                    "path": path,
                                    "header": header
                                })
            with open("mods.json", "w") as f:
                json.dump(save_data, f, indent=4)
            if __name__ == "__main__":
                print("Mods discovered and added.\n")
            return

        # Convert selection to int for toggling mods
        selection = int(selection)
        if selection == 0 and __name__ == "__main__":
            print("Exiting mod manager.")
            sys.exit(0)

        if 1 <= selection <= len(mods["mods"]):
            selected_mod = mods["mods"][selection - 1]
            selected_mod["enabled"] = not selected_mod.get("enabled", False)
            with open("./mods.json", "w") as f:
                json.dump(mods, f, indent=4)
            if __name__ == "__main__":
                print(f"Mod '{selected_mod['name']}' is now {'ENABLED' if selected_mod['enabled'] else 'DISABLED'}.\n")
        elif __name__ == "__main__":
            print("Selection out of range.")
            
    except (ValueError, IndexError, TypeError):
        print("Invalid input. Please try again.")
if __name__ == "__main__":
    while True:
        mod(input("Enter mod number to toggle it, or 'd' to discover mods, or 0 to exit: "))
