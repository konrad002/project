
from PyQt5.QtWidgets import *
import select

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
import json
from datetime import datetime

from src_client.states import *
from src_client.ui import run_app
def send(self, message):
          
          if(message == ""):
               return
          if(len(message) > 256):
               alert3 = QMessageBox()
               alert3.setText("Message is too long.\n\nMaximum length is 256.")
               alert3.exec_()
               self.message.setText("")
               return
        
          print(len(self.states.messagesSent))
          
          timeSent = datetime.now().strftime("%H:%M")
        
        
          #alert = QMessageBox()
          #for i, j, k in messagesSent:
          #    userSecond = datetime.strptime(k, "%H:%M:%S")
          #    print(userSecond, new)
          #    if(new >= userSecond and len(messagesSent) >1):
          #        alert.setText("Sending too fast")
          #        alert.exec_()
          #        message = ""
                

          self.states.messagesSent.append(("client", self.states.username_input, message, timeSent))
          sending = {
             "user": "client",
             "username" : self.states.username_input,
             "message" : message,
             "time": timeSent
          }
        
        
          try:
               data = json.dumps(sending)
               if(not data):
                    print("no data in sending")
                    return
               self.states.s.sendall(data.encode("utf-8"))
               print("sent from client")
          except Exception as e:
               print(e)
               self.message.setText("")  

        
          print("does this get run here?")
          print(self.states.messagesSent)
          self.message.setText("")
          self.new_signal.emit(message)  

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
                              

                              QTimer.singleShot(0, self.parse_temp)
                              QTimer.singleShot(0, self.change_ui_later)
                              QTimer.singleShot(0, self.disconnections)
                              
                              
                              
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

def relogin(self):
    if(os.path.exists("temp/temp-client.json")):
               with open('temp/temp-client.json', 'r') as output:
                    r = json.load(output)
                    self.states.username_input = r[0]["client_user"]
                    self.states.client_username = r[0]["server_user"]   
                   
                    f = r[1:len(r)]     
                    for k in f:
                    
                         self.states.messagesSent.append((k["user"], k["username"], k["message"], k["time"]))


                    print(r)
                
                
                
                    self.states.loading = True
                    print("run?")
                    print(self.states.messagesSent)
                    output.close()
            
            
            
            
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
                    

              
                
               print("do we ever get here?")             
            
            
            
               print("tiems?")
               
               run_app(self)
            
            
               return  