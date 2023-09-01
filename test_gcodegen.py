import random

gstring = ''
interval = 5
max_x = 665
min_x = 150

count = int((max_x - min_x) / interval)
for i in range(count):
    j = round((i * interval), 2) + min_x
    gstring += f"G1 F2300.0 X{min_x} Y{0} Z-3.3\n"
    gstring += f"G1 F2300.0 X{j} Y{0} Z-3.3\n"
    gstring += f"G1 F2300.0 X{j} Y{j} Z-3.3\n"
    gstring += f"G1 F2300.0 X{min_x} Y{j} Z-3.3\n"
    
print(gstring)

f = open('bigtest.gcode', 'w')
f.write(gstring)
