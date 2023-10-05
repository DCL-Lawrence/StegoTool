# StegoTool
## Introduction
This is a function library which implement the image, audio and network header steganography. Generally, you should add the file into the project that you want to use the functions. Each type of have their own library which are Graph, Audio, and Stream in order. All the library contain a class which the name is same as the file. You can use the follow command to write your code.
## Usage
### Iamge steganography:
<ol>
  <li>Declare the object: s = Graphy(name_of_a_image)</li>
  <li>Select the used channels: s.select("R:2 / G:1 / B:1")</li>
  <li>Reselect the used channels: s.reselect("R:2 / G:1 / B:1")</li>
  <li>Hide the secret data with hiding sequence and generate a image which contains secret data: s.create("132", secret_data)</li>
  <li>Extract the secret data with hiding sequence into secret.txt: s.get("132") </li>
</ol>

### Audio steganography:
<ol>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ol>

### Network header steganography
<ol>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ol>
