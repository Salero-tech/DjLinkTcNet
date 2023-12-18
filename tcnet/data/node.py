from dataclasses import dataclass
from tcnet.data.message import message
import time

@dataclass
class Node:
    ip:str
    created:int
    port:int
    id: int
    name: str

    def __init__(self, msg:message) -> None:
        self.ip = msg.ip
        self.port = msg.data.listenerPort
        self.id = msg.header.id
        self.name = msg.header.name
        #get time of data
