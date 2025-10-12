import json
import os
import sys
import pickle

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

def compile_mod(mod_dir):
    manifest_path = os.path.join(mod_dir, "manifest.json")
    if not os.path.isfile(manifest_path):
        print(f"No manifest.json in {mod_dir}")
        return False
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    mod_data = {
        "name": manifest["name"],
        "version": manifest["version"],
        "description": manifest.get("description", ""),
        "id": manifest["id"],
        "compatible": manifest["compatible"],
        "incompatible": manifest["incompatible"],
        "main": "",
        "init": "",
        "on_advance": ""
    }
    for key in ["main", "init", "on_advance"]:
        file_path = os.path.join(mod_dir, manifest[key].split("/")[-1])
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read()
                # Replace relative paths in code to absolute or remove dependencies
                content = content.replace('./mods/', './').replace('./manifest.json', '').replace('./mods/examplemod/manifest.json', '').replace('./mods/arcade/manifest.json', '').replace('with open("./examplemod/manifest.json") as f:\n    manifest = json.load(f)\n\nmod.__init__(manifest["name"])', 'mod.__init__("example mod")').replace('with open("./arcade/manifest.json") as f:\n    manifest = json.load(f)\n\nmod.__init__(manifest["name"])', 'mod.__init__("arcade")')
                mod_data[key] = content
        else:
            print(f"Missing {key} file: {file_path}")
            return False
    mod_file = os.path.join(mod_dir, f"{manifest['name'].replace(' ', '')}.mod")
    with open(mod_file, "wb") as f:
        pickle.dump(mod_data, f)
    print(f"Compiled {manifest['name']} to {mod_file}")
    return True

def mod(selection):
    import glob
    mod_files = glob.glob("./mods/*/*.mod") + glob.glob("./mods/*/*.mod.disabled")
    mods = []
    for mod_file in mod_files:
        with open(mod_file, "rb") as f:
            header = pickle.load(f)
        enabled = not mod_file.endswith(".disabled")
        mods.append({
            "name": header["name"],
            "enabled": enabled,
            "file": mod_file
        })
    if __name__ == "__main__":
        print("\n=== MOD MANAGER ===")
        for i, mod in enumerate(mods):
            status = "ON" if mod["enabled"] else "OFF"
            print(f"{i+1}. {mod['name']} [{status}]")

    try:

        if selection == "d":
            mods_path = os.path.join(os.path.dirname(__file__), "mods")
            for entry in os.listdir(mods_path):
                full_path = os.path.join(mods_path, entry)
                if os.path.isdir(full_path):
                    compile_mod(full_path)
            if __name__ == "__main__":
                print("Mods discovered and compiled.\n")
            return

        if selection == "c":
            mods_path = os.path.join(os.path.dirname(__file__), "mods")
            for entry in os.listdir(mods_path):
                full_path = os.path.join(mods_path, entry)
                if os.path.isdir(full_path):
                    compile_mod(full_path)
            if __name__ == "__main__":
                print("Mods compiled.\n")
            return

        # Convert selection to int for toggling mods
        selection = int(selection)
        if selection == 0 and __name__ == "__main__":
            print("Exiting mod manager.")
            sys.exit(0)

        if 1 <= selection <= len(mods):
            selected_mod = mods[selection - 1]
            if selected_mod["enabled"]:
                new_file = selected_mod["file"] + ".disabled"
                os.rename(selected_mod["file"], new_file)
                selected_mod["enabled"] = False
                selected_mod["file"] = new_file
            else:
                new_file = selected_mod["file"].replace(".disabled", "")
                os.rename(selected_mod["file"], new_file)
                selected_mod["enabled"] = True
                selected_mod["file"] = new_file
            if __name__ == "__main__":
                print(f"Mod '{selected_mod['name']}' is now {'ENABLED' if selected_mod['enabled'] else 'DISABLED'}.\n")
        elif __name__ == "__main__":
            print("Selection out of range.")
            
    except (ValueError, IndexError, TypeError):
        print("Invalid input. Please try again.")
if __name__ == "__main__":
    while True:
        mod(input("Enter mod number to toggle it, 'd' to discover mods, 'c' to compile mods, or 0 to exit: "))
