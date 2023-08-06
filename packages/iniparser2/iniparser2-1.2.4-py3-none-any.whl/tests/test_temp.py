from iniparser2 import INI_TEMP

tmp = INI_TEMP()
data = tmp.parse("""
temp=IxHdgTszZ1oz

[main]
data=400
""")

print(data)