from StegoTool import Graph
import sys

data = ""

with open(sys.argv[2], "r") as file:
    for line in file:
        data += line

d = ""
for i in range(len(data)):
    d += bin(ord(data[i]))[2:].zfill(8)

img = Graph(sys.argv[1])
img.select("R:2 / G:1 / B:2")
img.create("12", d)
img.save_image("New" + sys.argv[1])

img.get("12")
