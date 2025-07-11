mapping_table = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December"
}
import json
import pickle
from random import randint
from os import system, name, path
import binformatlib
import os
import random
from datetime import datetime
from cryptography.fernet import Fernet as fernet


def check_key():
    if not os.path.exists(os.path.join(os.path.dirname(__file__),"key")):
        with open("key","wb") as f:
            key = fernet.generate_key()
            f.write(key)
    with open("key","rb") as f:
        key = fernet(f.read())
    return key
key = check_key()
datetime = datetime.now()
def regenerate_junk_sections():
    return {
        ".text": random.randbytes(random.randint(128, 4096)),
        ".bss": random.randbytes(random.randint(64, 1024)),
        ".mem": random.randbytes(random.randint(64, 1024)),
    }
with open("settings.json","r") as f:
    settings = json.load(f)

clear = settings.get("clear", False)

def safe_to_hex(value):
    if isinstance(value, bytes):
        return value.hex()
    else:
        return str(value).encode('utf-8').hex()

VERSION = "2.0.1"

custom_format = {
    "metadata": {
        "version": VERSION,
        "required_mods": [],
    },
    "magic": b"T\x53yco\x7Fon\xaaSa\x1ave",
    "data": None,
    "EOS":b"\x00\xFF\xde\xe0\x00\x11\x22\x33"
}
money = 0

establishments = {
    "store": {"cost": 1000, "income": 100, "upkeep": 50, "loan": 100},
    "restaurant": {"cost": 5000, "income": 500, "upkeep": 200, "loan": 300}
}

save = {
    "money": 1000,
    "owned_establishments": {},
    "month": datetime.month,
    "loans": [1000],
    "year":datetime.year,
    "income":0
}

# --- SAVE ---

def save_game():
    global money, month, loans, required, save, custom_format
    custom_format.update(regenerate_junk_sections())
    save["money"] = money
    save["month"] = month
    save["loans"] = loans
    save["year"] = year

    custom_format["metadata"]["required_mods"] = ",".join(required)

    os.makedirs("./saves", exist_ok=True)
    filename = input("enter save name: ").strip()
    if not filename:
        print("Invalid filename")
        return
    if not filename.endswith(".save"):
        filename += ".save"

    filepath = f"{os.path.dirname(__file__)}/saves/{filename}"
    try:
        binformatlib.pack(custom_format, filepath, pickle.dumps(save))
        print(f"Game saved to {filepath}")
    except Exception as e:
        print(f"[save] error: {e}")

# --- LOAD ---

def load_game():
    global money, month, loans, required, save, custom_format
    filename = input("enter save name: ").strip()
    if not filename:
        print("Invalid filename")
        return False

    if not filename.endswith(".save"):
        filename += ".save"

    filepath = f"{os.path.dirname(__file__)}/saves/{filename}"

    if not os.path.exists(filepath):
        print(f"[load] File does not exist: {filepath}")
        return False
    try:
        unpacked = binformatlib.unpack(filepath)
    except Exception as e:
        try:
            with open(filepath,"rb") as f:
                decrypted = key.decrypt(f.read())
                save = json.loads(decrypted)
        except Exception as e:
            print(f"[load] error: {e}")

    if not unpacked or not isinstance(unpacked, dict):
        print(f"[load] Failed to load file: {filepath}")
        return False
    save_required_bytes = unpacked.get("metadata", {}).get("required_mods", b"")
    save_required_str = save_required_bytes.decode("utf-8") if isinstance(save_required_bytes, bytes) else save_required_bytes
    save_required = save_required_str.split(",") if save_required_str else []

    if not all(mod in required for mod in save_required):
        print("Missing required mods, cannot load save.")
        return False

    try:
        loaded_save = pickle.loads(unpacked["data"])
    except Exception as e:
        print(f"[load] Failed to unpickle save data: {e}")
        return False

    save.clear()
    save.update(loaded_save)
    money = save.get("money", 0)
    month = save.get("month", 0)
    loans = save.get("loans", [])
    year = save.get("year",1)

    print(f"Game loaded from {filepath}")
    return True

year = save["year"]
month = save["month"]
money = save["money"]
loans = save["loans"]
income = save["income"]
# Load mods
with open("./mods.json") as f:
    mods = json.load(f)

choices = ["buy", "sell", "save", "load", "advance", "quit", "loan"]
code = []
advance_code = []
dont_load = []
required = []

for mod in mods["mods"]:
    if mod["enabled"]:
        if mod["name"] in dont_load:  # placeholder, dangerous because load order matters
            continue

        with open(mod["header"], "r") as f:
            header = json.load(f)

        # Check incompatibilities
        incompatible_found = False
        for mod_check in mods["mods"]:
            with open(mod_check["header"], "r") as f_check:
                mod_check_header = json.load(f_check)
                if header["id"] in mod_check_header.get("incompatible", []):
                    dont_load.append(mod_check_header["name"])
                    incompatible_found = True
        if incompatible_found:
            continue

        if VERSION not in header.get("compatible", []):
            continue

        with open(header["main"], "r") as f:
            code.append(f.read())

        with open(header["init"], "r") as f:
            exec(f.read())

        with open(header["on_advance"], "r") as f:  # Fixed the syntax error here
            advance_code.append(f.read())

        required.append(header["name"])

print("mods loaded")



while True:
    print(f"{mapping_table[month]}:{year}")
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
        save_game()
    elif choice == "load":
        load_game()

    elif choice == "advance":
        month += 1
        # Income/upkeep per owned establishment
        for est in save["owned_establishments"]:
            for _ in range(save["owned_establishments"][est]):
                money += establishments[est]["income"]
                income += establishments[est]["income"]
                money -= establishments[est]["upkeep"]
                if money <= -5000:
                    print("you went bankrupt")
                    quit()
                if money <= 0:
                    money += 1000
                    income += 500
                    for _ in range(10):
                        save["loans"].append(50)
                    input("you got a 5000 dollar loan to get you out of debt, press enter to continue...")
        new_loans = []
        for loan in loans:
            repayment = loan // 2
            money -= repayment
            remaining = loan - repayment
            if remaining > 0:
                new_loans.append(remaining)
        loans = new_loans
        if month > 12:
            year += 1
            month = 1
            if income > 0:
                money += 0.8 * income
            else:
                money *= 0.8 if money > 0 else 1
            income = 0
        for mod_code in advance_code:
            exec(mod_code)
    elif choice == "quit":
        quit()
    elif choice == "loan":
        amount = int(input("how much money would you like to loan: "))
        if amount <= 10_000:
            loans.append(amount)
            money += amount
        else:
            print("loan too big")
    if clear and os.name == "nt":
        os.system("cls")
    elif clear:
        os.system("clear")
