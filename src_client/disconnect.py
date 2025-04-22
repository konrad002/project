import socket
from PyQt5.QtWidgets import *

import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import json

import os
import time

from src_client.states import *


def trying(self):
          print("jason 2")
          print(self.thread.is_alive)
          if(self.thread.is_alive() == False):
               print(self.states.s)
               self.thread = threading.Thread(target=self.receive, daemon = True)
               self.thread.start()   
               print("jason")
               
def disconnections(self):
          self.states.s = None
          print("disconnections called how many times?")
          
          
           
          if(self.states.count > 0):
               self.states.count = 0
          else: 
               
               self.states.count = self.states.count + 1
          reconnected = False
          self.states.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          
          for k in [1, 2, 4, 8, 12]:
               time.sleep(k)
                          
               try:
                    print(1)
                    self.states.s.connect((self.states.HOST, 12345))
                    print(2)
                    ready = self.states.s.recv(1024).decode()
                    
                    print("f2")
                    if(ready == "ready"):
                         self.states.s.sendall(b"confirmed")
                         reconnected = True                                                                                                
                         break
                         
                        
                              
               except:
                    print("exception")
                     
          print("done")
          print(reconnected)
          if(reconnected == False):
               exit()
                     
          self.states.loading = False
          self.states.state1 = True
          print(self.states.s.getpeername())
          print(11)
          self.reset()
                
                
          print(44)
          print(self.states.s.getpeername())
          
          self.trying()
          print(self.thread.is_alive)
          
def reset(self):
          global navbar
          navbar.clear() 
          navbar.addMenu(self.states.username_input)
          
          

def parse_temp(self):
          with open('temp/temp-client.json', 'w') as output:
               if(os.path.getsize("temp/temp-client.json")):
                  os.remove("temp/temp-client.json")
                  output.close()
               message_list = []
               sending = {
                       "client_user": self.states.username_input,
                       "server_user" : self.states.client_username
               }
               self.states.pastConnections["client"] = sending["client_user"]
               self.states.pastConnections["server"] = sending["server_user"]
               message_list.append(sending)
                
               

               for something in self.states.messagesSent:
                    sending = {
                        "user": something[0],
                        "username" : something[1],
                        "message" : something[2],
                        "time" : something[3]
                    }
                    message_list.append(sending)
               print(message_list)
               if(message_list == []):
                    output.close()
                    os.remove("temp/temp-client.json")
                    print("ooga booga?")
                    exit()
                     
               print("when does this get run?")
               json.dump(message_list, output, indent=4)
                                          
                                 
               output.close()