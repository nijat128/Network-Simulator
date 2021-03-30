# CP372
# Names: Nijat Abdulkarimli, Asad Abbas
# ID: 160584230, 160498330
from common import *

class receiver:
    ACK = 0
    SEQ = 0
    expectedSeqNum = 0

    def isCorrupted(self, packet):
        #  Check if a received packet has been corrupted during transmission.
        # Return true if computed checksum is different than packet checksum.
        checksum = checksumCalc(packet.payload) + (packet.ackNum + packet.seqNum)
        if checksum == packet.checksum:
            return True
        else:
            return False


    def isDuplicate(self, packet):
        #check if packet sequence number is the same as expected sequence number
        if packet.seqNum == self.expectedSeqNum:
            return True
        else:
            return False


    def getNextExpectedSeqNum(self):
        #Use modulo-2 arithmetic to ensure sequence number is 0 or 1.
        if self.expectedSeqNum % 2 == 0:
            return 1
        else:
            return 0


    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self):
        # initialise expected packet sequence number
        self.expectedSeqNum = 0
        return

    def input(self, packet):
        # This method will be called whenever a packet sent from the sender
        # arrives at the receiver.
        # If packet is corrupted or duplicate: send ACK with the last ack number of
        # last correctly received packet. In other words, you can say send
        # a packet with wrong sequence number as there is only 0 and 1.
        # If packet is OK (not a duplicate or corrupted), deliver it and send
        # correct ACK.
        if self.isCorrupted(packet) is True or self.isDuplicate(packet) is True:
            if packet.seqNum == 0:
                i = 1
            else:
                i = 0
            packet = Packet(i, self.ACK, self.ACK + packet.seqNum, "")
        else:
            packet = Packet(packet.seqNum, self.ACK, self.ACK + packet.seqNum, "")
            self.expectedSeqNum = self.getNextExpectedSeqNum()
        self.networkSimulator.udtSend(B, packet)

        return
