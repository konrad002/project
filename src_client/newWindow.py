import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import keyboard
import json
from datetime import datetime
import os
import time

from src_client.states import *
from src_client.ui import ui_chatApp
from src_client.disconnect import parse_temp, disconnections

class newWindow(QMainWindow):
     new_signal = pyqtSignal(str)
     def __init__(self):
            
          super().__init__()
          
          self.states = states
          
          self.handler = False
          
          self.new_signal.connect(self.update_label)

          self.thread = threading.Thread(target=self.receive, daemon = True)
          self.thread.start()
          #self.sidebar = sidebarWindow()
           #part of main layout, sidebar
          ui_chatApp(self)
          
          
          

     def ui_(self):
          
          pass
          
     
          
          

     def closeEvent(self, event):
          print("z2")
          parse_temp(self)
          event.accept()     

            
     def update_label(self): #TODO: Fix this god awful code.
                       
          
          print(self.states.messagesSent, "fsagf")       
            
          if(self.states.loading == False):

               for user, username, msg, time in self.states.messagesSent[-1:]:
                    print(msg)
                    print(user)
                  
            
                    print(self.states.loading)
                    if(user == "client"):
                              
                         print("run?, how many times?")
                        
                         self.label = QLabel(username + ": "+ msg + "  \n " + time)
                        
                         self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                         self.main_layout.addWidget(self.label)
                    else:

                         print(msg)
                        
                         self.label = QLabel(username + ": "+ msg + " \n  " + time)
                         self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                         self.main_layout.addWidget(self.label)
          else:
               print("fsagetg")
               for user, username, msg, time in self.states.messagesSent:
                        
                    if(user == "client"):
                         print("run?, how many times?")
                        
                         self.label = QLabel(username + ": "+ msg + "  \n " + time)
                        
                         self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                         self.main_layout.addWidget(self.label)
                    else:
                         print(msg)
                        
                         self.label = QLabel(username + ": "+ msg + " \n  " + time)
                         self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                         self.main_layout.addWidget(self.label)

               self.states.loading = False
     

           
                 
     def change_ui_later(self):
          self.banner.setAlignment(Qt.AlignCenter)
          self.banner.setStyleSheet("""
                                    QLabel{
                                    background-color: #cc3333;
                                    color: #ffffff;
                                    padding: 4px;
                                    font-weight: bold;
                                    border-bottom: 0.5px solid #ccc;
                                    }
                                    """)
          self.banner.show()      
     
     def receive(self):
        
          
          while True:
                  

                  ready, _, _ = select.select([self.states.s], [], [], 0.5)
                  

                  print(ready, "this is ready")
                        
                  if(ready):
                        
                        try:
                              
                                   
                              data = self.states.s.recv(1024)
                              if(not data):
                                   print("server has disconnected.")
                                   return
                              print(data, "this is data")
                             
                              print("connection closed")
                                   
                             
                             
                        except Exception as e:
                              print(e)
                              print("z?")
                              print(e)
                              

                              parse_temp(self)
                              QTimer.singleShot(0, self.change_ui_later)
                              disconnections(self)
                              
                              
                              
                              break
                        print(data)
                        
                        
                        message = json.loads(data.decode("utf-8"))
                        print(message)
                        user = message["user"]
                        self.states.username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        self.states.messagesSent.append((user, self.states.username, message_received, timeSent2))
                        print(self.states.messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")