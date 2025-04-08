from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import json
from datetime import datetime
import os

from src_client.states import *
from src_client.ui import ui_window, run_app

from src_client.network import relogin

class Window(QWidget):
     def __init__(self):
          super().__init__()
          
          self.states = states
          self.reconnecting = False
          
          
        
        
          if(os.path.exists("temp/temp-client.json")):
               self.reconnecting = True
               self.rr()
            

          if(self.reconnecting == False):
               ui_window(self)
               print(self.reconnecting, "this is self.reconnecting")
          self.on_click()
     

     def rr(self):
          
          label_username = QMessageBox()
          label_username.setIcon(QMessageBox.Information)
          label_username.setText("Want to relogin to past connection?")
          label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
          r = label_username.exec_()
          if(r == QMessageBox.Ok):
               self.states.isReady = False
               self.on_click()
               return
          elif(r == QMessageBox.Cancel):
               os.remove("temp/temp-client.json")
               exit()
          else:
              pass
    
     
     
     def on_click(self):
          alert = QMessageBox()
          
        
          self.states.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
     
             
          if(self.states.client != None):
               print("does this get run?")
               exit()
                        
        
        
    
          relogin(self)

          try:
            
               print("???")
            
               self.states.s.connect((self.textbox1.text(), int(self.textbox2.text())))
            
               
               print(self.states.pastConnections)
               self.states.username_input = self.textbox3.text()
               self.states.pastConnections["user"] = "client"
               self.states.pastConnections["client"] = self.states.username_input
               self.states.pastConnections["server"] = self.states.client_username
               
               if(self.states.username_input == self.states.client_username):
                    print("client and server username's are the same!!!!")
               run_app(self)
               print("connected to server")
            

          except Exception:
               alert.setText("Wrong IP or port number! ")
               alert.setWindowTitle("Error")
               alert.setIcon(QMessageBox.Icon.Warning)
               alert.setStandardButtons(QMessageBox.StandardButton.Ok)
               alert.exec_()
            
          
     