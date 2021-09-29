from PIL import Image

colour_data = [
    {"r":127,"g":178,"b":56,"block":"slime_block"},
    {"r":247,"g":233,"b":163,"block":"birch_planks"},
    {"r":199,"g":199,"b":199,"block":"mushroom_stem"},
    {"r":255,"g":0,"b":0,"block":"redstone_block"},
    {"r":160,"g":160,"b":255,"block":"packed_ice"},
    {"r":167,"g":167,"b":167,"block":"iron_block"},
    {"r":0,"g":124,"b":0,"block":"oak_leaves[persistent=true]"},
    {"r":255,"g":255,"b":255,"block":"snow_block"},
    {"r":164,"g":168,"b":164,"block":"clay"},
    {"r":151,"g":109,"b":77,"block":"dirt"},
    {"r":112,"g":112,"b":112,"block":"stone"},
    {"r":143,"g":119,"b":72,"block":"oak_planks"},
    {"r":255,"g":252,"b":245,"block":"diorite"},
    {"r":216,"g":127,"b":51,"block":"orange_wool"},
    {"r":178,"g":76,"b":216,"block":"magenta_wool"},
    {"r":102,"g":153,"b":216,"block":"light_blue_wool"},
    {"r":229,"g":229,"b":51,"block":"yellow_wool"},
    {"r":127,"g":204,"b":25,"block":"lime_wool"},
    {"r":242,"g":127,"b":165,"block":"pink_wool"},
    {"r":76,"g":76,"b":76,"block":"gray_wool"},
    {"r":153,"g":153,"b":153,"block":"light_gray_wool"},
    {"r":76,"g":127,"b":153,"block":"cyan_wool"},
    {"r":127,"g":63,"b":178,"block":"purple_wool"},
    {"r":51,"g":76,"b":178,"block":"blue_wool"},
    {"r":102,"g":76,"b":51,"block":"brown_wool"},
    {"r":102,"g":127,"b":51,"block":"green_wool"},
    {"r":153,"g":51,"b":51,"block":"red_wool"},
    {"r":25,"g":25,"b":25,"block":"black_wool"},
    {"r":250,"g":238,"b":77,"block":"gold_block"},
    {"r":92,"g":219,"b":213,"block":"diamond_block"},
    {"r":74,"g":128,"b":255,"block":"lapis_block"},
    {"r":0,"g":217,"b":58,"block":"emerald_block"},
    {"r":129,"g":86,"b":49,"block":"spruce_planks"},
    {"r":112,"g":2,"b":0,"block":"netherrack"},
    {"r":209,"g":177,"b":161,"block":"white_terracotta"},
    {"r":159,"g":82,"b":36,"block":"orange_terracotta"},
    {"r":149,"g":87,"b":108,"block":"magenta_terracotta"},
    {"r":112,"g":108,"b":138,"block":"light_blue_terracotta"},
    {"r":186,"g":133,"b":36,"block":"yellow_terracotta"},
    {"r":103,"g":117,"b":53,"block":"lime_terracotta"},
    {"r":160,"g":77,"b":78,"block":"pink_terracotta"},
    {"r":57,"g":41,"b":35,"block":"gray_terracotta"},
    {"r":135,"g":107,"b":98,"block":"light_gray_terracotta"},
    {"r":87,"g":92,"b":92,"block":"cyan_terracotta"},
    {"r":122,"g":73,"b":88,"block":"purple_terracotta"},
    {"r":76,"g":62,"b":92,"block":"blue_terracotta"},
    {"r":76,"g":50,"b":35,"block":"brown_terracotta"},
    {"r":76,"g":82,"b":42,"block":"green_terracotta"},
    {"r":142,"g":60,"b":46,"block":"red_terracotta"},
    {"r":37,"g":22,"b":16,"block":"black_terracotta"},
    {"r":189,"g":48,"b":49,"block":"crimson_nylium"},
    {"r":148,"g":63,"b":97,"block":"crimson_planks"},
    {"r":92,"g":25,"b":29,"block":"crimson_hyphae"},
    {"r":22,"g":126,"b":134,"block":"warped_nylium"},
    {"r":58,"g":142,"b":140,"block":"warped_planks"},
    {"r":86,"g":44,"b":62,"block":"warped_hyphae"},
    {"r":20,"g":180,"b":133,"block":"warped_wart_block"},
    {"r":100,"g":100,"b":100,"block":"deepslate"},
    {"r":216,"g":175,"b":147,"block":"raw_iron_block"}
]

def RGBToHSV(red, green, blue):
    r = red / 255
    g = green / 255
    b = blue / 255
    v = max(r, g, b)
    cmin = min(r, g, b)
    delta = v - cmin
    h = 0
    s = 0
    if r == g and g == b:
        h = 0
    elif v == r:
        h = 60 * ((g - b) / delta % 6)
    elif v == g:
        h = 60 * ((b - r) / delta + 2)
    else:
        h = 60 * ((r - g) / delta + 4)
    if v == 0:
        s = 0
    else:
        s = delta / v
    return [h,s,v]

def GetHSVColour(colour, multiplier, shade):
    hsv = RGBToHSV(colour["r"] * multiplier, colour["g"] * multiplier, colour["b"] * multiplier)
    return {"h":hsv[0], "s":hsv[1], "v":hsv[2], "block":colour["block"], "shade":shade}

def SetupColours(colour_data):
    i = 0
    hsv_colours = []
    for colour in colour_data:
        hsv_colours.append(GetHSVColour(colour, 1, -1))
        hsv_colours.append(GetHSVColour(colour, 0.86, 0))
        hsv_colours.append(GetHSVColour(colour, 0.71, 1))
        i = i + 1
    return hsv_colours

def GetBlockColour(pixel, colour_array):
    closestIndex = -1
    closestHSV = 10000
    i = 0
    for colour in colour_array:
        hueDistance = min(abs(pixel[0] - colour["h"]) - abs(pixel[1] - colour["s"] * 7) - abs(pixel[2] - colour["v"] * 2), abs(pixel[0] - colour["h"] + 360) - abs(pixel[1] - colour["s"] * 7) - abs(pixel[2] - colour["v"] * 2))
        if hueDistance < closestHSV:
            closestHSV = hueDistance
            closestIndex = i
        i = i + 1
    return closestIndex

def ReadPixel(x, y):
    return RGBToHSV(pixels[x,y][0], pixels[x,y][1], pixels[x,y][2])
    
colours = SetupColours(colour_data)
height_levels = [128] * 128

pixels = Image.open('test_image.png').load()

commands = ""
for i in range(-64, 64):
    commands = commands + "fill -64 1 " + str(i) + " 63 255 " + str(i) + " air\n"
    
for y in range(0, 128):
    for x in range(0, 128):
        number = GetBlockColour(ReadPixel(x, y), colours)
        commands = commands + "setblock " + str(x-64) + " " + str(height_levels[x]) + " " + str(y-64) + " " + str(colours[int(number)]["block"]) + "\n"
        height_levels[x] = height_levels[x] + colours[int(number)]["shade"]

f = open("imagetomap.mcfunction", "w")
f.write(commands)
f.close()