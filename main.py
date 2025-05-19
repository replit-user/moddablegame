import json
from random import randint
from os import system, name, path,getcwd
money = 0

VERSION = "alpha"



establishments = {
    "store":
        {
        "cost":1000,
        "income":100,
        "upkeep":75
        },
    "restaurant":
        {"cost":5000,
                  "income":500,
                  "upkeep":250
                  }
    }

save = {
    "money":1000,
    "owned_establishments":{
        "store":
        0,
        "restaurant":
            0
        },
    "month":0
}

month = save["month"]
money = save["money"]


with open("./mods.json") as f:
    mods = json.load(f)

for mod in mods["mods"]:
    if mod["enabled"]:
        with open(mod["header"],"r") as f:
            header = json.load(f)
            if VERSION not in header["compatible"]:
                continue
            else:
                with open(header["main"],"r") as f:
                    exec(f.read())

print("mods loaded")


while True:
    print("month " + str(month))
    print("money " + str(money))
    choices = ["buy","sell","save","load","advance","quit"]
    for choice in choices:
        print(choice)
    choice = input(">")
    if choice not in choices:
        print("invalid choice")
        continue
    elif choice == "buy":
        for establishment in establishments:
            print(establishment)
        establishment = input("establishment> ")
        if establishment not in establishments:
            print("invalid establishment")
        else:
            money -= establishments[establishment]["cost"]
            save["owned_establishments"][establishment] += 1
            
    elif choice == "sell":
        for establishment in save["owned_establishments"]:
            if save["owned_establishments"][establishment] > 0:
                print(establishment)
        establishment = input("establishment> ")
        if not establishment in save["owned_establishments"] or save["owned_establishments"][establishment] == 0:
            print("invalid establishment")
        else:
            money += establishments[establishment]["cost"] // 2
            save["owned_establishments"][establishment] -= 1
    elif choice == "save":
        with open("./save.json","w") as f:
            data = json.dumps(save)
            f.write(data)
    elif choice == "load":
        with open("./save.json","r") as f:
            save = f.read()
            save = json.loads(save)
            money = save["money"]
            month = save["month"]
    elif choice == "advance":
        for establishment in save["owned_establishments"]:
            for i in range(save["owned_establishments"][establishment]):
                money += establishments[establishment]["income"]
                money -= establishments[establishment]["upkeep"]
                if money <= 0:
                    print("you lose")
                    quit()
    elif choice == "quit":
        quit()
    if name == "nt":
        system("cls")
    else:
        system("clear")