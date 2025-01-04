from StegoTool import Stream
import sys

data = ""

with open(sys.argv[2], "r") as file:
    for line in file:
        data += line

d = ""
for i in range(len(data)):
    d += bin(ord(data[i]))[2:].zfill(8)

s = Stream(sys.argv[1])
s.select("IPv6(hlim:8, plen:16)")
s.create("12", d)
s.save_pcap("New" + sys.argv[1])

s.get("12")
