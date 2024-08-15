from StegoTool import Stream
import sys

s = Stream(sys.argv[1])
s.select("IPv6(hlim:8, plen:16)")
s.create("12", "I have a pen.")
s.save_pcap("New" + sys.argv[1])
s.get("21")
