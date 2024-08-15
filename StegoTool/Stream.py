from scapy.all import *
from math import pow
from dataclasses import dataclass

@dataclass
class Stream:
    def __init__(self, pcap):
        # Prepare a data stream in a pcap file.
            packets = rdpcap(pcap)
        
            self.packets:list = []
            self.header:list = []    # The headers for selected channels.
            self.field:list = []     # The selected channels
            self.nbits:list = []     # The number of hidden bits for each channel.
            self.data:str = ""       # Binary string
            for packet in packets:
                self.packets.append(packet)

    # Sample input: DNS()/UDP(sport)/IPv6(hlim,plen)
    def select(self, Packet) -> None:
        Packet = Packet.replace(' ', '')
        Packet = Packet.split('/')

        for label in Packet:
            # Get header and fields.
            Htemp = label[:label.find('(')]
            temp = label[label.find('(') + 1 : label.find(')')] 
            Ftemp = temp.split(',')

            if(len(temp) > 0):
                for i in Ftemp:
                    # Store field with header.
                    (self.header).append(Htemp)
                    i = i.split(':')
                    (self.field).append(i[0])
                    (self.nbits).append(int(i[1]))
            else:
                continue

    def reselect(self, Packet) -> None:
        self.header = []
        self.field = []
        self.nbits = []
        self.select(Packet)

    def hiding(self, packet, header, field, nbits, number):
        # Processing data hiding.
        value = getattr(packet[header], field)
        setattr(packet[header], field, int(value - value % pow(2, nbits)) + number)

        return packet

    # Input the hopping sequence and secret data.
    def check(self, sequence, data): 
        # Calculate wether the length of data exceed length of stream ot not.
        P = [] # The length for a period.
        for i in sequence:
            P.append(self.nbits[int(i) - 1])

        L = len(sequence)
        D = len(data) # Remove parity check bit.
        N:int = L * (D // sum(P))
        left:int = D % sum(P)
        count:int = 0

        for i in range(L):
            if(left > 0):
                count += 1
                left -= P[i]
            else:
                break

        if(N + count > len(self.packets)):
            return False, None, None

        return True, left, N + count

    # Default using single channel.
    def create(self, sequence, data) -> None:
        # Check the data can be hidden or not.
        check, left, count = self.check(sequence, data)
        if(check == False):
            raise RuntimeError("The data is too long to hide into the stream you gave.")

        binstr:str = data
        
        # Padding with 0.
        for i in range(abs(left)):
            binstr += '0'

        for i in range(count):
            index =  int(sequence[i % len(sequence)]) - 1

            # The bit string that is going to be used in this round.
            string = binstr[0 : self.nbits[index]]
            self.packets[i] = self.hiding(self.packets[i], self.header[index], self.field[index], self.nbits[index], int(string, 2))
            # Cut off the part which has been hidden.
            binstr = binstr[self.nbits[index] :]


    def save_pcap(self, filename):
        wrpcap(filename, self.packets)

    def extracting(self, packet, header, field, nbits) -> int:
        value = int(getattr(packet[header], field) % pow(2, nbits))

        return value

    def get(self, sequence) -> str:
        bits:str = ""
        for i in range(len(self.packets)):
            index =  int(sequence[i % len(sequence)]) - 1
            value = self.extracting(self.packets[i], self.header[index], self.field[index], self.nbits[index])
            bits += bin(value)[2:].zfill(self.nbits[index])

        self.data = bits

        return self.data