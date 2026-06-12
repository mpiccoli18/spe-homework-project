# Script for generate the buildings in the city

block_size = 150
building_size = 100
blocksNum = 2

with open("buildings.poly.xml", "w") as f:
    f.write("<additional>\n")
    id = 0
    for x in range(blocksNum):
        for y in range(blocksNum):
            xPos = (x * block_size) + 25
            yPos = (y * block_size) + 25
            
            shape = f"{xPos}, {yPos} {xPos + building_size}, {yPos} {xPos + building_size}, {yPos + building_size}"
            f.write(f'     <poly id = "building_{id}" type = "building" color="179, 179, 179" fill = "1" layer = "-1" shape="{shape}"/>\n')
            id += 1
        f.write("</additional>\n")

    
print("Buildings generated successfully!")