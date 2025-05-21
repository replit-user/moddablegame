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
        "upkeep":50,
        "loan":100
        },
    "restaurant":
        {"cost":5000,
                  "income":500,
                  "upkeep":200,
                  "loan":300
                  }
    }

save = {
    "money":1000,
    "owned_establishments":{
        },
    "month":0,
    "loans":[]
}

month = save["month"]
money = save["money"]
loans = save["loans"]

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


choices = ["buy","sell","save","load","advance","quit","loan"]
while True:
    print("month " + str(month))
    print("money " + str(money))
    for choice in choices:
        print(choice)
    choice = input("> ").lower()
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
            if not establishment in save["owned_establishments"]:
                save["owned_establishments"][establishment] = 0
            save["owned_establishments"][establishment] += 1
            loans.append(establishments[establishment]["loan"])
            
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
        with open(f"./saves/{input("eenter save name: ")}.json","w") as f:
            save["money"] = money
            save["month"] = month
            data = json.dump(save,f,indent=4)
    elif choice == "load":
        with open(f"./saves/{input("enter save name: ")}.json","r") as f:
            save = f.read()
            save = json.loads(save)
            money = save["money"]
            month = save["month"]
            loans = save["loans"]
    elif choice == "advance":
        for establishment in save["owned_establishments"]:
            for i in range(save["owned_establishments"][establishment]):
                money += establishments[establishment]["income"]
                money -= establishments[establishment]["upkeep"]
                if money <= 0:
                    money += 1000
                    for i in range(10):
                        loans.append(50)
                    input("you got a 1000 dollar loan to get you out of debt, press enter to continue... ")
        for i in range(loans.count(0)):
            loans.remove(0)
            
        i = 0
        for loan in loans:
            money -= loan // 2
            loans[i] = loans[i] // 2
            i += 1
        month += 1
    elif choice == "quit":
        quit()
    elif choice == "loan":
        ammount = int(input("how much money would you like to loan: "))
        loans.append(ammount)
        money += ammount
    if name == "nt":
        system("cls")
    else:
        system("clear")