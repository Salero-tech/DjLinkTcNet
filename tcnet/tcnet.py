from tcnet.data.message import message
from tcnet.data.node import Node
from tcnet.data.mHeader import mHeader
import threading
import socket
from tcnet.datObj import DataObj

UDP_IP = ""
UDP_PORT = 60000

class tcNet:
  send_Lock = threading.Lock()
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

  #self
  dataObj = DataObj()

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
    try:
      #read header
      data, addr = self.sock.recvfrom(mHeader.HEADER_WITH) # buffer size
      header = mHeader.fromBytes(data)
      #read data
      data, addr = self.sock.recvfrom(message.getDataSize(header)) # buffer size is 1024 bytes
      #remove own data
      if (header.id == self.dataObj.id):
        return
      #with self.recCache_Lock:
      self.recCache.append(message.fromBytes(header ,data, addr[0]))
    except:
      print("fail to read")
      return

  def send (self, ip:str, port:int, data:bytes):
    with self.send_Lock:
      self.sock.sendto(data,(ip, port))

  #logic
  def handleRec (self):
    if self.recCache.__len__() <= 0:
      return
    msg = self.recCache.pop(0)
    #node list
    if msg.typeAsStr == "optIn":
       self.addNodeToList(msg)
       return
    if msg.typeAsStr == "optOut":
       self.removeNodeFromList(msg)
       return
    print("data?")
       
  def addNodeToList (self, msg:message):
    #check if alread in list if so update last contact
    for node in self.nodeList:
      if node.id == msg.header.id:
        node = Node(msg)
        return
    #add to list
    self.nodeList.append(Node(msg))
         
  def removeNodeFromList (self, msg:message):
      removeNodeIndex:int = None
      for node, i in enumerate(self.nodeList):
        if node.id == msg.header.id:
           removeNodeIndex = i
           break
      if removeNodeIndex is not None:
        self.nodeList.pop(removeNodeIndex)

  def sendStatusPacket (self):
    self.send("192.168.178.255", 60000, self.dataObj.statusPacket)

  def sendOptIn (self):
    self.send("192.168.178.255", 60000, self.dataObj.optIn)
    #broadcast + to all nodes on listening port
    for node in self.nodeList:
      self.send(node.ip, node.port, self.dataObj.optIn)

  def sendOptOut (self):
    self.send("192.168.178.255", 60000, self.dataObj.optOut)
    #broadcast + to all nodes on listening port
    for node in self.nodeList:
      self.send(node.ip, node.port, self.dataObj.optOut)

  def sendMetaData (self):
    for node in self.nodeList:
      self.send(node.ip, node.port, self.dataObj.metaData)

  def sendMetricData (self):
    for node in self.nodeList:
      self.send(node.ip, node.port, self.dataObj.MetricData)

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
      #send status packet
      self.sendStatusPacket()
      #self.sendMetaData()
      #self.sendMetricData()
      #thread start
      threading.Timer (
        1, # ever 1000ms
        self.KeepAliveThread,
        ).start()
      
  def __del__ (self):
     self.stopKeepAliveThread()
     self.stopRecThread()