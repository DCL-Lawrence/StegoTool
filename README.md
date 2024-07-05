# StegoTool
## Introduction
This is a function library which implement the image, audio and network header steganography. 
<br> Generally, you should add the file into the project that you want to use the functions. 
<br> Each type of have their own library which are Graph, Audio, and Stream in order. 

------
## Import:
The import statement will same as following.
1. Image: `from StegoTool import Graph`
2. Audio: `form StegoTool import Audio`
3. Network header: `from StegoTool import Stream`

## Initialzation:
Firstly, you shall declare a variable for each types of method. The parameter for the class is a file path. You should give the corresponded types of file. (.png, .wav, and .pcap)
1. Image: `image = Graph(in.png)`
2. Audio: `audio = Audio(in.wav)`
3. Network header: `stream = Stream(in.pcap)`

## Select target channels and bits:
Secondly, you have to choose the used channels and bits for data hiding or extracting.
1. Image: `image.select("R:2 / G:1 / B:1") # Select last 2 bits in red and last 1 bit for both green and blue channel.`
2. Audio: `audio.select("121") # Select last 2 bits in second and 1 bit for both first and third sound channel.`
3. Network header: `stream.select("IPv6(hlim:8, plen:16)") # Select 8 bits in Hop Limit and 16 bits in Payload Length of IPv6.`
