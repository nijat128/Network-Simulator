# CP372
from common import *

class sender:
    ACK = 0
    RTT = 20
    currentSeqNum = 0
    currentPacket = 0

    def isCorrupted (self, packet):
        #  Check if a received packet (ACK) has been corrupted during transmission.
        # similar to the corresponding function in receiver side
        checksum = checksumCalc(packet.payload) + (packet.ackNum + packet.seqNum)

        if checksum == packet.checksum:
            return True
        else:
            return False


    def isDuplicate(self, packet):
        # checks if an ACK is duplicate or not
        #similar to the corresponding function in receiver side
        #2 points
        if packet.ackNum == self.ACK:
            return True
        else:
            return False


    def getNextSeqNum(self):
        # generate the next sequence number to be used
        # similar to the corresponding function in receiver side
        if self.currentSeqNum % 2 == 0:
            return 1
        else:
            return 0


    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        #initialize the currentSeqNum  and currentPacket
        self.currentSeqNum = 0
        self.currentPacket = None
        return

    def timerInterrupt(self):
        # This function implements what the sender does in case of timer interrupt
        # It sends the packet again.
        # It starts the timer, sets the timeout value to be twice the RTT
        self.networkSimulator.udtSend(A, self.currentPacket)
        self.networkSimulator.startTimer(A, self.RTT*2)
        return

    def output(self, message):
        # prepare a packet and send the packet through the network layer
        # call utdSend
        # start the timer
        # you must ignore the message if there is one packet in transit
        checksum = checksumCalc(message.data) + (self.currentSeqNum + self.ACK)
        packet = Packet(self.currentSeqNum, self.ACK, checksum, message.data)
        self.networkSimulator.udtSend(A, packet)
        self.networkSimulator.startTimer(A, self.RTT)
        return

    def input(self, packet):
        # If ACK isn't corrupted or duplicate, transmission complete.
        # timer should be stopped, and sequence number  should be updated
        # In the case of duplicate ACK the packet, you do not need to do
        # anything and the packet will be sent again since the
        # timerInterrupt will be called by the simulator.
        if self.isCorrupted(packet) is True or self.isDuplicate(packet) is True:
            self.networkSimulator.udtSend(A, packet)
        else:
            self.currentPacket = None
            self.currentSeqNum = self.getNextSeqNum()
            self.networkSimulator.stopTimer(A)

        return
