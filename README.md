## PATCH NOTES

##### 2.0.5
  
-    added a personal message from me to the end of readme.md(you have no idea how much I tried not to cry when writing it)
  
-    change version number to 2.0.5

##### 2.0.4
  
-    change version to 2.0.4
  
-    fixed a small bug, what was the bug?

-    for users:
  
-    sometimes your money was multiplied by a negative number so when yearly taxes came your money would increase

-    for mod devs:

-    the variable 'income' would be negative if your gross was less than 0 due to loans or otherwise, this would result in money -= 0.8 * [SOME NEGATIVE NUMBER]

-   how it was fixed(devs only):

-    added an if statement to check if income is bigger than 0, if it is leave it alone, otherwise make it 0 essentially 'clamping' the minimum to 0

-    added more save obfuscation using junk keys

# Tycoon Console Game

A simple console-based tycoon game in Python with mod support, save/load functionality, and an expandable codebase.

---

## Features

- Buy and sell establishments to grow your income  
- Manage loans and finances  
- Advance months and years with income and upkeep calculations  
- Save and load game state using a custom binary format with encryption  
- Support for mods to extend gameplay  
- Simple mod manager to enable/disable and discover mods  

---

## Installation

1. Make sure you have Python 3.8 or higher installed.  
2. Clone or download this repository, or in realeses download the install script for your platform and run the script with the instilation path as the first argument
3. Install required dependencies with:

```bash
pip install binformatlib cryptography
```

---

## Running the Game

Run the main script:

```bash
python main.py
```

The game will load available mods and then present you with a menu of commands.

---

## Gameplay Controls

At the prompt, choose from the following commands:

-   `buy` — Purchase an establishment
    
-   `sell` — Sell one of your owned establishments
    
-   `save` — Save your current game progress
    
-   `load` — Load a saved game
    
-   `advance` — Advance the game by one month (calculates income, upkeep, loans, etc.)
    
-   `loan` — Take a loan to increase your money (max $10,000)
    
-   `quit` — Exit the game
    

---

## Save System

-   Saves are stored in the `./saves/` folder as `.save` files.
    
-   Save files use a custom binary format for integrity and encryption via the `cryptography` library.
    
-   When saving, you are prompted to enter a filename.
    
-   When loading, the game checks for required mods and verifies compatibility.
    

---

## Modding

Mods are Python-scripted expansions packaged with metadata that extend or modify game behavior.

### Mod Structure

Each mod resides in its own folder under `./mods/` and must contain at least the following files:

-   `manifest.json` — Contains mod metadata such as:
    
    -   `name` (string): Mod name
        
    -   `version` (string): Mod version
        
    -   `compatible` (list of strings): Compatible game versions (e.g., `["2.0.2"]`)
        
    -   `id` (string): Unique mod identifier
        
    -   `main` (string): Path to main script file relative to the mod folder
        
    -   `init` (string): Path to initialization script
        
    -   `on_advance` (string): Path to script run on advancing the game month
        
    -   `incompatible` (optional, list of strings): List of mod IDs this mod conflicts with
        
-   Python script files as referenced in `manifest.json`
    

### How Mods Work

-   The game loads all enabled mods on startup, running their init scripts and keeping their main and advance scripts in memory.
    
-   During gameplay, the main mod scripts run every loop iteration.
    
-   Advance scripts run every time the player advances the month.

### a note to keep in mind

your scripts are ran using the 
```python

exec()

```

function so you can easily modify game variables and more, HOWEVER

this means you need to make sure:

- all paths are absoulute OR
- all paths are relative to ./main.py



    

### Creating a Mod

1.  Create a new folder in `./mods/`, e.g., `./mods/my_mod/`
    
2.  Add a `manifest.json` describing your mod. Example:
    

```json
{
  "name": "My Cool Mod",
  "version": "1.0.0",
  "compatible": ["2.0.2"],
  "id": "my_cool_mod",
  "main": "main.py",
  "init": "init.py",
  "on_advance": "advance.py",
  "incompatible": []
}
```

3.  Add your Python scripts (`main.py`, `init.py`, `advance.py`) implementing your mod logic.
    
4.  Run the mod manager (`python manager.py`), enter `d` to discover mods, then enable your mod.
    
5.  Start the game to see your mod in action.
    

---

## Mod Manager

Manage your mods using the included `manager.py` script:

```bash
python manager.py
```

Commands inside the mod manager:

-   Enter a mod number to toggle it ON/OFF
    
-   Enter `d` to discover and add new mods from the `./mods/` folder
    
-   Enter `0` to exit the manager
    

The game will only load mods marked as enabled.

---

## Development & Future Plans

-   Improve gameplay mechanics and balance
    
-   Enhance modding documentation
    
-   Add more establishments and features
    
-   Polish user interface and error handling
    

---

## Contributing

submit pull requests but I'm one person with a strict schedule so I might not review it right away, also feel free to fork and/or suggest changes to my email: umyashinderu@gmail.com

---

## License

MIT liscense

---

*Enjoy building your tycoon empire!*



## special note

this project was never meant to be even moderately big as it is, it was meant for me to learn how to implement modding into a simple game, but I added more features, heck I coded my own python module because there wasn't one that did exactly what I want, and then I extend it, fix bugs, add features that were never meant to be, I am not 100% sure but I think I started this as a school project, I've been working on it for 6 months with maybe a spur of updates one day a month, heck the moment I grasp C++ I might just port this hole project over from scratch, anyway, my point is that this project never would've gone this far(which it hasn't gone mcuh far at all but I hope it will go further) and I want you to keep in mind these things while playing this super small super simple game that doesn't even have a GUI or TUI but a CLI(trust me as someone who uses the unix terminal, cli's are not fun) 
