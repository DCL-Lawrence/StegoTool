from StegoTool import Audio
import sys

a = Audio(sys.argv[1])
a.select("121") # Use first channel 1 bit, second channel 2 bits and third channel 1 bit.
a.create("213", "I have a pen.")
a.select_audio_list(["New1svega.wav", "New2svega.wav", "New3svega.wav"])
a.get("213")
