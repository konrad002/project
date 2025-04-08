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
from src_client.ui import ui_chatApp
from src_client.states import *
from src_client.network import receive
class newWindow(QMainWindow):
     new_signal = pyqtSignal(str)
     def __init__(self):
            
          super().__init__()
          
          self.states = states
          
          self.handler = False
          
          self.new_signal.connect(self.update_label)

          self.thread = threading.Thread(target=receive, daemon = True)
          self.thread.start()
          #self.sidebar = sidebarWindow()
          self.ui_chatApp() #part of main layout, sidebar
          
          ui_chatApp(self)
          
          

     def ui_(self):
          
          pass
          
     
          
          

     def closeEvent(self, event):
          print("z2")
          self.parse_temp()  
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
     