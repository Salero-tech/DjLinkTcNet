from tcnet.data.message import message
from tcnet.data.node import Node
import threading
import socket

UDP_IP = "192.168.178.29"
UDP_PORT = 60000

class tcNet:
  #socket
  sock:socket.socket
  sock_Lock = threading.Lock()
  #alive
  alive = False
  alive_Lock = threading.Lock()
  #receive
  receiveActive = False
  receive_Lock = threading.Lock()
  #receive
  recCache:list[message] = []
  recCache_Lock = threading.Lock()
  #nodes
  nodeList:list[Node] = []

  def __init__(self) -> None:
    self.createSocket()
    self.startRecThread()
    self.startKeepAliveThread()

  #sockets
  def createSocket (self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # internet/UDP
    self.sock.bind((UDP_IP, UDP_PORT))
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def receive (self):
    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
    #with self.recCache_Lock:
    self.recCache.append(message(data, addr))

  def send (self, ip:str, port:int, data:bytes):
    self.sock.sendto(data,(ip, port))
     

  #logic
  def loop (self):
    #handle keep alive
    #with self.recCache_Lock:
    if self.recCache.__len__() > 0:
      self.handleRec()

  def handleRec (self):
    msg = self.recCache.pop(0)
    #node list
    if msg.typeAsStr == "optIn":
       self.addNodeToList(msg)
       return
    if msg.typeAsStr == "optOut":
       self.removeNodeFromList(msg)
       return
       
  def addNodeToList (self, msg:message):
    #check if alread in list if so update last contact
    for node in self.nodeList:
      if node.id == msg.header.id:
        #update stuff
        return
    #add to list
    self.nodeList.append(Node(msg))
         
  def removeNodeFromList (self, msg:message):
      removeNode:node = None
      for node in self.nodeList:
        if node.id == msg.header.id:
           removeNode = node
           break
      if removeNode is not None:
        self.nodeList.remove(removeNode)

  def sendOptIn (self):
    self.send("192.168.178.255", 60000, b"hello")
    #broadcast + to all nodes on listening port
    print("optin")

  def sendOptOut (self):
    print("optout")


  #thread stuff
  def startRecThread (self):
    with self.receive_Lock:
      self.receiveActive = True
    self.recThread()

  def stopRecThread (self):
     with self.receive_Lock:
        self.receiveActive = False

  def recThread (self):
      #check if stoped
      with self.receive_Lock:
        if self.receiveActive == False:
          return

      #send opt in
      self.receive()
      #thread start
      threading.Timer (
        1, # ever 1000ms
        self.recThread,
        ).start()

  def stopKeepAliveThread (self):
    with self.alive_Lock:
        self.alive = False

  def startKeepAliveThread (self):
    with self.alive_Lock:
        self.alive = True
    #start
    self.KeepAliveThread()

  def KeepAliveThread (self):
      #check if stoped
      with self.alive_Lock:
        if self.alive == False:
          self.sendOptOut()
          return

      #send opt in
      self.sendOptIn()
      #thread start
      threading.Timer (
        1, # ever 1000ms
        self.KeepAliveThread,
        ).start()
      
  def __del__ (self):
     self.stopKeepAliveThread()
     self.stopRecThread()