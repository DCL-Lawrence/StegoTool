import cv2
import math
from dataclasses import dataclass

@dataclass
class Graph():
    def __init__(self, filename):
        self.img = cv2.imread(filename) #numpy array

        self.row:int = 0
        self.col:int = 0
        self.color:int = 0
        self.row, self.col, self.color = self.img.shape

        self.channel:list = []
        self.nbits:list = []

        self.data:str = ""  # Binary string

    # Sample input: R:N/G:N/B:N
    def select(self, seq) -> None:
        seq = seq.replace(' ', '')
        temp = seq.split('/')
        
        for con in temp:
            if(con[0] == 'R'):
                self.channel.append(2)
            elif(con[0] == 'G'):
                self.channel.append(1)
            elif(con[0] == 'B'):
                self.channel.append(0)
            else:
                raise ValueError(f"Invalid specific channel {con[0]}")

            if(int(con[2]) <= 2):
                self.nbits.append(con[2])
            else:
                raise ValueError(f"Channel {con[0]} use {con[2]} bits is longer than 2.")

    def reselect(self, seq) -> None:
        self.select(seq)

    # The maxmim value for  bit is two.
    # Variable number is the secret data.
    def hiding(self, pixel, bit ,number) -> int:
        pixel -= (pixel % math.pow(2, bit))
        return pixel + number

    def check(self, sequence, data):
        P = []
        for i in sequence:
            P.append(int(self.nbits[int(i) - 1]))

        L = len(sequence)
        D = len(data)
        N = L * (D // sum(P))
        left:int = D % sum(P)
        count:int = 0

        for i in range(L):
            if(left > 0):
                count += 1
                left -= P[i]
            else:
                break

        if(N + count > self.col * self.row):
            return False, None, None
        else:
            # Return the number of bits need be filled and the number of pixel used.
            return True, left, N + count

    def create(self, sequence, data) -> None:
        check, left, count = self.check(sequence, data)
        if(check == False):
            raise RuntimeError("The data is too long to hide into the image you gave")

        binstr:str = data

        # Padding with 0
        for i in range(abs(left)):
            binstr += '0'

        Cindex:int = 0 # Column index
        Rindex:int = 0 # Row index
        for i in range(count):

            index = int(sequence[i % len(sequence)]) - 1
            # Get length of current field.
            use = int(self.nbits[index])

            # The bit string that is going to be used in this round.
            string = binstr[0:use]
            # Get pixel value
            pixel = self.img[Rindex][Cindex][self.channel[index]]
            self.img[Rindex][Cindex][ self.channel[index] ] = self.hiding(pixel, use, int(string, 2))

            # Cut off the part which has been hidden
            binstr = binstr[use:]
            
            # Adjust index
            Cindex += 1
            if(Cindex // self.col == 1):
                Cindex = 0
                Rindex += 1

    def save_image(self, filename) -> None:
        cv2.imwrite(filename, self.img)

    def extracting(self, pixel, bit) -> int:
        return int(pixel % math.pow(2, bit))
    
    def get(self, sequence) -> str:
        Cindex:int = 0 # Column index
        Rindex:int = 0 # Row index
        binstr:str = ""

        for i in range(self.col * self.row):
            index = int(sequence[i % len(sequence)]) - 1
            
            # Get length of current field.
            use = int(self.nbits[index])
                        
            pixel = self.img[Rindex][Cindex][self.channel[index]]
            value = self.extracting(pixel, use)
            binstr += bin(value)[2:].zfill(use)

            Cindex += 1
            if(Cindex // self.col == 1):
                Cindex = 0
                Rindex += 1
        
        self.data = binstr
        
        return self.data