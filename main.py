import json
import pickle
from random import randint
from os import system, name, path
import binformatlib
def safe_to_hex(value):
    if isinstance(value, bytes):
        return value.hex()
    else:
        return str(value).encode('utf-8').hex()
VERSION = "1.1.0"

custom_format = {
    "metadata": {
        "version": VERSION,
        "required_mods": []
    },
    "eos": "hgVcBmKP",
    "data": None
}

money = 0

establishments = {
    "store": {"cost": 1000, "income": 100, "upkeep": 50, "loan": 100},
    "restaurant": {"cost": 5000, "income": 500, "upkeep": 200, "loan": 300}
}

save = {
    "money": 1000,
    "owned_establishments": {},
    "month": 0,
    "loans": [1000]
}

required = []
month = save["month"]
money = save["money"]
loans = save["loans"]

# Load mods
with open("./mods.json") as f:
    mods = json.load(f)

choices = ["buy", "sell", "save", "load", "advance", "quit", "loan"]
code = []

for mod in mods["mods"]:
    if mod["enabled"]:
        with open(mod["header"], "r") as f:
            header = json.load(f)
            if VERSION not in header["compatible"]:
                continue
            with open(header["main"], "r") as f:
                code.append(f.read())
            with open(header["ready"], "r") as f:
                exec(f.read())
            required.append(header["name"])

print("mods loaded")

while True:
    print("month", month)
    print("money", money)
    for choice in choices:
        print(choice)
    choice = input("> ").lower()

    if choice not in choices:
        print("invalid choice")
        continue

    elif choice == "buy":
        for est in establishments:
            print(est, establishments[est]["cost"])
        est = input("establishment> ")
        if est not in establishments:
            print("invalid establishment")
        else:
            money -= establishments[est]["cost"]
            save["owned_establishments"].setdefault(est, 0)
            save["owned_establishments"][est] += 1
            loans.append(establishments[est]["loan"])

    elif choice == "sell":
        for est in save["owned_establishments"]:
            if save["owned_establishments"][est] > 0:
                print(est)
        est = input("establishment> ")
        if est not in save["owned_establishments"] or save["owned_establishments"][est] == 0:
            print("invalid establishment")
        else:
            money += establishments[est]["cost"] // 2
            save["owned_establishments"][est] -= 1

    elif choice == "save":
        save["money"] = money
        save["month"] = month
        save["loans"] = loans

        # Replace the list of mods with a string so it can be hex-encoded
        custom_format["metadata"]["required_mods"] = ",".join(required)

        # Pickle and pack the save data
        data = pickle.dumps(save)
        filename = input("enter save name: ") + ".save"
        binformatlib.pack(custom_format, f".\saves\{filename}", data)



    elif choice == "load":
        unpacked = binformatlib.unpack(custom_format, filename)

        if not unpacked or not isinstance(unpacked, dict):
            print(f"[load] Failed to load file: {filename}")
            continue  # skip loading and return to menu

        # Check required mods
        save_required = unpacked.get("metadata", {}).get("required_mods", [])

        if not all(mod in required for mod in save_required):
            print("Missing required mods, cannot load save.")
        else:
            save = pickle.loads(unpacked["data"])
            money = save["money"]
            month = save["month"]
            loans = save["loans"]

    elif choice == "advance":
        for est in save["owned_establishments"]:
            for i in range(save["owned_establishments"][est]):
                money += establishments[est]["income"]
                money -= establishments[est]["upkeep"]
                if money <= -5000:
                    print("you went bankrupt")
                    quit()
                if money <= 0:
                    money += 1000
                    for _ in range(10):
                        loans.append(50)
                    input("you got a 1000 dollar loan to get you out of debt, press enter to continue...")

        loans = [loan // 2 for loan in loans if loan // 2 > 0]
        month += 1

    elif choice == "quit":
        quit()

    elif choice == "loan":
        amount = int(input("how much money would you like to loan: "))
        if amount <= 10_000:
            loans.append(amount)
            money += amount
        else:
            print("loan too big")

    for mod_code in code:
        exec(mod_code)

    if name == "nt":
        system("cls")
    else:
        system("clear")
