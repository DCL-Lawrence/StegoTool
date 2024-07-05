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

        self.data:str = ""  # Binary string

        # Sound files list
        self.list = []

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
        D = len(data)
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

        binstr:str = data
        
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
    
    def select_audio_list(self, flist):
        self.list = flist

        if(len(self.list) != self.nChannel):
            raise ValueError("The number of sound files is not matched to the number of channels.")

    def get(self, sequence) -> str:
        binstr:str = ""

        for i in range(self.nChannel):
            self.rate, self.sound = wavfile.read(self.list[i])
            self.sounds[i] = self.sound

        for i in range(len(self.sound)):
            index = int(sequence[i % len(sequence)]) - 1
            
            # Get length of current field.
            use = int(self.nbits[index])

            amplitude = self.sounds[index][i]
            value = self.extracting(amplitude, use)
            binstr += bin(value)[2:].zfill(use)
        
        self.data = binstr

        return self.data