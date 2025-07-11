from sys import argv
filename = argv[1]

with open(f"./saves/{filename}.save","r") as f:
    hexdata = f.read()

# Decode hex to bytes
data = bytes.fromhex(hexdata)

# Convert bytes to string safely for metadata parsing
try:
    text = data.decode('utf-8', errors='ignore')
except:
    text = ""

lines = text.splitlines()

metadata = {}
binary_sections = {}
current_section = None
bin_data = bytearray()

for line in lines:
    if "=" in line and current_section is None:
        key, val = line.split("=", 1)
        metadata[key.strip()] = val.strip()
    elif line.startswith("."):
        if current_section:
            binary_sections[current_section] = bin_data
            bin_data = bytearray()
        current_section = line.strip(".")
    else:
        if current_section:
            bin_data += line.encode('utf-8')

if current_section:
    binary_sections[current_section] = bin_data

print("Metadata:")
for k,v in metadata.items():
    print(f"  {k}: {v}")

print("\nSections:")
for sec, bdata in binary_sections.items():
    print(f"  {sec}: {len(bdata)} bytes")
