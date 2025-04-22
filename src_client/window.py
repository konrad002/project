from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import json
from datetime import datetime
import os
import bcrypt
from src_client.states import *
from src_client.ui import ui_window, ui_chatApp
from src_client.newWindow import newWindow
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

          
     

     def rr(self):
          
          label_username = QMessageBox()
          label_username.setIcon(QMessageBox.Information)
          label_username.setText("Want to relogin to past connection?")
          label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
          r = label_username.exec_()
          if(r == QMessageBox.Ok):
               self.states.isReady = False
               self.on_click()
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
          if(os.path.exists("temp/temp-client.json")):

               relogin(self)
          else:
               self.hashed = bcrypt.hashpw(self.password.text().encode("utf-8"), bcrypt.gensalt())
               self.states.client_password = self.hashed.decode()
               print(self.states.client_password)
          

               try:
            
                    print("???")
            
                    self.states.s.connect((self.states.HOST, 12345))
            
               
                    print(self.states.pastConnections)
                    print(16)
                    self.states.username_input = self.textbox3.text()
                    print(15)
                    sending = self.states.username_input + self.states.client_password
                    self.states.s.sendall(sending.encode("utf-8"))
                    print(17)
                    self.states.pastConnections["user"] = "client"
                    self.states.pastConnections["client"] = self.states.username_input
                    print(19)
                    self.states.pastConnections["server"] = self.states.client_username
                    print(18)
               
                    self.close()
                    print(1)
                    self.client = newWindow()
                    print(2)
               
                    print(3)
                    self.client.show()
               
                    print(4)
                    print("connected to server")
            

               except Exception:
                    alert.setText("Wrong IP or port number! ")
                    alert.setWindowTitle("Error")
                    alert.setIcon(QMessageBox.Icon.Warning)
                    alert.setStandardButtons(QMessageBox.StandardButton.Ok)
                    alert.exec_()
            
          
     