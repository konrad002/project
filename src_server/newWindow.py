import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import select
import keyboard
import json
from datetime import datetime
import os
import time
from src_server.states import *
from src_server.core import ui_newWindow
from src_server.disconnect import parse_temp, disconnections

class newWindow(QMainWindow):
      
      new_signal = pyqtSignal(str)  
      def __init__(self, instance):
            
            super().__init__()
            print("d")
            self.states = states
            
            self.instance = instance
            
            self.new_signal.connect(self.update_label)
            
            self.thread2 = threading.Thread(target= self.receive, daemon = True)
            self.thread2.start() 

            ui_newWindow(self)

            
            
                  
            
                 
      def call_window(self):
            self.instance.connect()
      
      def closeEvent(self, event):
            print("z2")
            parse_temp(self)  
            event.accept()

      

            
      
      
         
      def update_label(self): # TODO: Fix this awful code please. 1 loop is bad enough
                          
            
            print(self.states.messagesSent)
            print("run during here?", self.states.loading)
            if(self.states.messagesSent != []):
                 pass
            
            if(self.states.loading == False):
                  for user, username, msg, time in self.states.messagesSent[-1:]:
                        print(msg)
                        print(user)
                  
            
                        print(self.states.loading)
                        if(user == "server"):
                              print("run?, how many times?")
                        
                              self.label = QLabel(username + ": "+ msg + "  \n " + time)
                        
                              self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                              self.client.addWidget(self.label)
                        else:
                              print(msg)
                        
                              self.label = QLabel(username + ": "+ msg + " \n  " + time)
                              self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                              self.client.addWidget(self.label)
            elif(self.states.loading == True):
                  for user, username, msg, time in self.states.messagesSent:
                  
                        if(user == "server"):
                              print("run?, how many times?")
                        
                              self.label = QLabel(username + ": "+ msg + "  \n " + time)
                        
                              self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                              self.client.addWidget(self.label)
                        else:
                              print(msg)
                        
                              self.label = QLabel(username + ": "+ msg + " \n  " + time)
                              self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                              self.client.addWidget(self.label)
                  self.states.loading = False
            else:
                  self.states.loading = False

      def receive(self):
 
          global data 
          while True:
                  

                  ready, _, _ = select.select([self.states.conn], [], [], 0.5)
                  

                  print(ready, "this is ready")
                        
                  if(ready):
                        
                        try:
                              
                                   
                              data = self.states.conn.recv(1024)
                              if(not data):
                                   print("client has disconnected.")
                                   return
                              print(data, "this is data")
                             
                              print("connection closed")
                                   
                             
                             
                        except Exception as e:
                              print(e)
                              print("z?")
                              print(e)
                              

                              parse_temp(self)
                              disconnections(self)
                              
                              
                              
                              break
                        print(data)
                        
                        
                        message = json.loads(data.decode("utf-8"))
                        print(message)
                        user = message["user"]
                        self.states.client_username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        self.states.messagesSent.append((user, self.states.client_username, message_received, timeSent2))
                        print(self.states.messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")
            
              
                  