import math
from scipy.io import wavfile
from dataclasses import dataclass

@dataclass
class Audio():
    def __init__(self, filename):
        self.sr:float = 0.0
        self.rate, self.sound = wavfile.read(filename)

        self.nChannel:int = 0

        # Different sound channels
        self.sounds = []

        self.nbits:list = []

        self.data:str = ""

    def select(self, seq) -> None:
        for i in range(len(seq)):
            if(int(seq[i]) <= 2):
                self.nbits.append(int(seq[i]))
            else:
                raise ValueError(f"Invalid bit used {seq[i]} is longer than 2.")
        self.nChannel = len(seq)

        # Setup each channel
        for i in range(self.nChannel):
            self.sounds.append(self.sound)

    def reselect(self, seq) -> None:
        self.select(seq)

    # The maxmim value for  bit is two.
    # Variable number is the secret data.
    def hiding(self, amplipude, bit ,number) -> float:
        amplipude -= (amplipude % math.pow(2, bit))
        return amplipude + float(number)

    def check(self, data):
        P = self.nbits

        L = len(P)
        D = 7 * len(data)
        N:int = L * (D // sum(P))
        left:int = D % sum(P)
        count:int = 0

        for i in range(L):
            if(left > 0):
                count += 1
                left -= P[i]
            else:
                break

        if(N + count > len(self.sound) * self.nChannel):
            return False, None, None
        else:
            # Return the number of bits need be filled and the number of pixel used.
            return True, left, N + count


    def create(self, sequence ,data) -> None:
        check, left, count = self.check(data)

        if(check == False):
            raise RuntimeError("The data is too long to hide into the audio you gave")

        # Convert data into bit stream
        binstr:str = ""
        for c in data:
            bits = bin(ord(c))[2:].zfill(7)
            binstr += bits
        
        # Padding with 0
        for i in range(abs(left)):
            binstr += '0'

        for i in range(count):
            index = int(sequence[i % len(sequence)]) - 1
            # Get length of current field.
            use = int(self.nbits[index])

            # The bit string that is going to be used in this round.
            string = binstr[0:use]

            amplitude = self.sounds[index][i]
            self.sounds[index][i] = self.hiding(amplitude, use, int(string, 2))

            # Cut off the part which has been hidden
            binstr = binstr[use:]

    def save_audio(self, filename) -> None:
        name = filename.split('.')[0]
        for i in range(self.nChannel):
            wavfile.write(name + str(i + 1) + ".wav", self.rate, self.sounds[i])

    def extracting(self, amplipude, bit) -> int:
        return int(amplipude % math.pow(2, bit))
    
    def get(self, sequence) -> None:
        binstr:str = ""

        for i in range(self.nChannel):
            self.rate, self.sound = wavfile.read(input("Input " + str(i + 1) + "th file: "))
            self.sounds[i] = self.sound

        for i in range(len(self.sound)):
            index = int(sequence[i % len(sequence)]) - 1
            
            # Get length of current field.
            use = int(self.nbits[index])

            amplitude = self.sounds[index][i]
            value = self.extracting(amplitude, use)
            binstr += bin(value)[2:].zfill(use)

        string:str = ""
        for i in range(0, len(binstr), 7):
            value = binstr[i:i+7]
            string += chr(int(value, 2))
        
        self.data = string

    def save_data(self, filename) -> None:
        open(filename, 'w').write(self.data)
