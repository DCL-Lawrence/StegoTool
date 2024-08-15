from StegoTool import Graph
import sys

img = Graph(sys.argv[1])
img.select("R:2 / G:1 / B:2")
img.create("12", "hello")
img.get("12")
