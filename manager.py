import json

def mod():
    with open("./mods.json", "r") as f:
        mods = json.load(f)

    print("\n=== MOD MANAGER ===")
    for i, mod in enumerate(mods["mods"]):
        status = "ON" if mod["enabled"] else "OFF"
        print(f"{i+1}. {mod['name']} [{status}]")

    try:
        selection = int(input("Enter mod number to toggle it (or 0 to exit): "))
        if selection == 0:
            exit()
        selected_mod = mods["mods"][selection - 1]
        selected_mod["enabled"] = not selected_mod["enabled"]
        with open("./mods.json", "w") as f:
            json.dump(mods, f, indent=4)
        print(f"Mod '{selected_mod['name']}' is now {'ENABLED' if selected_mod['enabled'] else 'DISABLED'}.\n")
    except (ValueError, IndexError):
        print("Invalid selection.")
        
        

while True:mod()