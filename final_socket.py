# Save as server.py 
# Message Receiver
import os
from socket import *
import time
host = "192.168.43.208"
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
while True:
    print "Waiting to receive messages..."
    (data, addr) = UDPSock.recvfrom(buf)
    print "Received message: " + data
    if data == "can":
        #print "frooti ka dabba"
        execfile("servo1.py")
        time.sleep(20)
        #break
    if data == "cardboard":
        execfile("servo2.py")
        #break
    if data == "plastic" :
        execfile("servo3.py")
        #break
UDPSock.close()

os._exit(0)

# Save as client.py 
# Message Sender
import os
from socket import *
host = "172.16.208.99" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = raw_input("Enter message to send or type 'exit': ")
    UDPSock.sendto(data, addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)