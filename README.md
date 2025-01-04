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

## Hide data:
In this step, you should decide the channel hiding sequence and prepare the secret message. (Note. The labels of the channel are determinded in the select target channels and bits step.)
1. Image: `image.create("12", b"I have a pen.") # Use sequence "12" to hide binary data "I have a pen.".`
2. Audio: `audio.create("213", b"I have a pen.") # Use sequence "213" to hide binary data "I have a pen.".`
3. Network header: `stream.create("12", b"I have a pen.") # Use sequence "12" to hide binary data "I have a pen.".`

## Export stego files::
After finish the data hiding step, you can export the stego files.
1. Image: `image.save_image(out.png)`
2. Audio: `audio.save_audio(out.wav) # This API will output multiple files`
3. Network header: `stream.save_pcap(out.pcap)`

## Extract data:
Also, you can extract the data from the target files like following samples.
1. Image: `data = image.get("12")`
2. Audio:
   ```
   audio.select_audio_list(["New1svega.wav", "New2svega.wav", "New3svega.wav"]) # Additional call with wave files (channels).
   data = audio.get("213")
   ```
3. Network header: `data = stream.get("12")`

## Additional function: Steganalysis tools
StegoTool also prove steganalysis APIs to detect the existence of hidden data. The current version contains Chi-square test and Rescaled range (RS) test
