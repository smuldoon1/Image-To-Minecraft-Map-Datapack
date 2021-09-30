from PIL import Image
import math
import os

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

def SetupColours(colour_data):
    colours = []
    for mapcolour in colour_data:
        colours.append({"Lab":RGBToLab([mapcolour["r"], mapcolour["g"], mapcolour["b"]]), "block":mapcolour["block"], "slope":1})
        colours.append({"Lab":RGBToLab([mapcolour["r"] * 0.86, mapcolour["g"] * 0.86, mapcolour["b"] * 0.86]), "block":mapcolour["block"], "slope":0})
        colours.append({"Lab":RGBToLab([mapcolour["r"] * 0.71, mapcolour["g"] * 0.71, mapcolour["b"] * 0.71]), "block":mapcolour["block"], "slope":-1})
    return colours

# RGB to XYZ to CIE-L*ab colour space conversion from http://www.easyrgb.com/en/math.php
def RGBToLab(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    if r > 0.04045:
        r = (r + 0.055) / 1.055 ** 2.4
    else:
        r = r / 12.92
    if g > 0.04045:
        g = (g + 0.055) / 1.055 ** 2.4
    else:
        g = g / 12.92
    if b > 0.04045:
        b = (b + 0.055) / 1.055 ** 2.4
    else:
        b = b / 12.92

    r = r * 100
    g = g * 100
    b = b * 100

    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 94.811
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 100.000
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 107.304

    if x > 0.008856:
        x = x ** (1/3)
    else:
        x = (7.787 * x) + (16 / 116)
    if y > 0.008856:
        y = y ** (1/3)
    else:
        y = (7.787 * y) + (16 / 116)
    if z > 0.008856:
        z = z ** (1/3)
    else:
        z = (7.787 * z) + (16 / 116)

    L = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return [L,a,b]

# Delta E* CIE colour comparison from http://www.easyrgb.com/en/math.php
def CompareColours(lab1, lab2):
    return math.sqrt(((lab1[0] - lab2[0]) ** 2) + ((lab1[1] - lab2[1]) ** 2) + ((lab1[2] - lab2[2]) ** 2))

def GetBlockColour(pixel, colours):
    matchedColour = {}
    minDelta = 10000
    i = 0
    for colour in colours:
        pixelLab = RGBToLab(pixel)
        deltaE = CompareColours(pixelLab, colour["Lab"])
        if deltaE < minDelta:
            minDelta = deltaE
            matchedColour = colour
    return matchedColour

colours = SetupColours(colour_data)
image_directory = "images"
image_files = []

for file in os.listdir(os.fsencode(image_directory)):
    filename = os.fsdecode(file)
    if (filename.endswith(".jpg") or filename.endswith(".png")):
        image_files.append(filename)

print("Converting " + str(len(image_files)) + " image file(s)")

for image_index in range(0, len(image_files)):
    image = Image.open(image_directory + "/" + image_files[image_index])
    resized_image = image.resize((128, 128))
    pixels = resized_image.load()

    height_levels = [128] * 128
    commands = ""
    for i in range(-64, 64):
        commands = commands + "fill -64 1 " + str(i) + " 63 255 " + str(i) + " air\n"
    
    for y in range(0, 128):
        for x in range(0, 128):
            colour = GetBlockColour(pixels[x, y], colours)
            commands = commands + "setblock " + str(x-64) + " " + str(height_levels[x]) + " " + str(y-64) + " " + colour["block"] + "\n"
            height_levels[x] = height_levels[x] + colour["slope"]
        print("Progress: " + "{:.2f}".format(100/(len(image_files)*128)*(image_index*128+y)) + "%")
    print("Finished converting " + str(image_index + 1) + " of " + str(len(image_files)) + " images")

    f = open(image_files[image_index] + ".mcfunction", "w")
    f.write(commands)
    f.close()

print("Image conversion succeeded")