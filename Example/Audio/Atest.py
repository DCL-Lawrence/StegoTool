from StegoTool import Audio
import sys

data = ""

with open(sys.argv[2], "r") as file:
    for line in file:
        data += line

# Binary data
d = ""
for i in range(len(data)):
    d += bin(ord(data[i]))[2:].zfill(8)

a = Audio(sys.argv[1]) # Use a convert audio file.
a.select("121") # Use first channel 1 bit, second channel 2 bits and third channel 1 bit.
a.create("213", d)
a.save_audio("New" + sys.argv[1])

a.select_audio_list(["New1svega.wav", "New2svega.wav", "New3svega.wav"])
a.get("213")
