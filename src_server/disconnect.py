from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import threading
import json
from datetime import datetime
import os
import time
from src_server.states import *
import bcrypt

  

def disconnections(self):
           
            
            self.states.conn = None
            print("disconnections called how many times?")
           
            
            
            self.states.isReady = False
            reconnected = False
            
            self.thread = threading.Thread(target=self.states.client_socket.call_window, daemon = True)
            self.thread.start()
            
           
            for k in [1, 2, 4, 8, 12]:
                  time.sleep(k)
                  print(self.thread.is_alive(), 1)
                  if(self.states.isReady):
                        reconnected = True
                        break
                  try:
                        
                        print(3)
                        self.states.conn.sendall(b"ready")
                        print(4)
                        reconnected = True
                        break
                              
                  except:
                        print("exception")

            if(not reconnected):
                  print("7")
                  QApplication.instance().quit()
            print(reconnected)          
            reconnected = False  
            
                     
             
            print("done")
            
            
                  
                  
            self.states.loading = False
            self.trying()
            print(self.thread2.is_alive)

def trying(self):

            if(self.thread2.is_alive() == False):
                  
                  self.thread2 = threading.Thread(target= self.receive, daemon = True)
                  self.thread2.start()                  

def parse_temp(self):
                
            with open('temp/temp-server.json', 'w') as output:
                  if(os.path.getsize("temp/temp-server.json")):
                        os.remove("temp/temp-server.json")
                        output.close()
           

                  else:
                  
                  
                  
                        message_list = []
                        sending = {
                              "client_user": self.states.client_username,
                              "server_user" : self.states.username
                        }
                        self.states.pastConnections["client"] = sending["client_user"]
                        self.states.pastConnections["server"] = sending["server_user"]
                        
                        message_list.append(sending)
                        
                        sending = {
                               "client_password" : self.states.client_password,
                               "server_password": self.states.server_password
                        }

                        message_list.append(sending)
                        for something in self.states.messagesSent:
                                          
                              sending = {
                                    "user" : something[0],
                                    "username" : something[1],
                                    "message" : something[2],
                                    "time" : something[3]
                                    }
                              message_list.append(sending)
                        print(message_list)
                        if(message_list == []):
                       
                              output.close()
                       
                              os.remove("temp/temp-server.json")
                       
                              exit()
                        print("when does this get run?")
                        json.dump(message_list, output, indent=4)
                                          
                        print(sending)
                                         
                        output.close()
