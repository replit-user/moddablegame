import json
class mod:
    def __init__(name):
        print("example mod loaded")

with open("./mods/examplemod/manifest.json") as f:
    manifest = json.load(f)

mod.__init__(manifest["name"])