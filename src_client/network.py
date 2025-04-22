
from PyQt5.QtWidgets import *
import select

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import json
from datetime import datetime

from src_client.states import *

from src_client.newWindow import newWindow




def relogin(self):
          

               while(self.states.isReady == False): #TODO
                    
                    label4 = QMessageBox()
                    label4.setText("Waiting to reconnect... 2 ")
                    label4.setStyleSheet("")
                    
                    label4.setWindowTitle(self.states.username_input + " "+ "relogin?")
                    
                    QTimer.singleShot(2000, label4.close)     
                    label4.exec_()  
                    print(self.states.s.fileno(), "gsgwe")
                    print(self.states.isReady)
                    
                    try:
                         
                         self.states.s.connect((self.states.HOST, 12345)) 
                         print("connected just now")
                         data = self.states.s.recv(1024).decode()
                         print(data)
                         if(data == "ready"):
                              print("ready s")
                              self.states.isReady = True
                         
                              self.states.s.sendall(b"confirmed")

                    

                    except Exception:
                         print("does it get an exception?")
                         pass
               
               receive = self.states.s.recv(1024).decode()
               f = receive.replace("'", '"')
               print(receive)
               data = json.loads(f)
               print(type(data), "this is what is in client rn")
               self.states.username_input = data[0]["client_user"]
               self.states.client_username = data[0]["server_user"]
               print(self.states.username_input, "0" , self.states.client_username)
                   
               f = data[2:len(data)]     
               for k in f:
                    
                    self.states.messagesSent.append((k["user"], k["username"], k["message"], k["time"]))


               print(receive)
                
                
                
               self.states.loading = True
               print("run?")
               print(self.states.messagesSent)
               
                     
            
            
            
               print("tiems?")
               
               self.close()
               self.client = newWindow()
               
               self.client.show()
            
               print(87)
               return  