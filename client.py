import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import *
import keyboard
import json
from datetime import datetime
import os
import time





hostname = str(socket.gethostname())
HOST = socket.gethostbyname(hostname)


class States:
      def __init__(self):
            self.s = None
            self.state0 = False
            self.loading = False
            self.client = None
            self.client_username = ""
            self.isReady = None
            self.username = ""
            self.r = ""
            self.messagesSent = []
            self.pastConnections = {}
            self.username_input = ""
            self.count = 0
            

states = States()

class window(QWidget):
     def __init__(self):
          super().__init__()
          
          self.states = states
          self.reconnecting = False
          
          
        
        
          if(os.path.exists("temp-client.json")):
               self.reconnecting = True
               self.rr()
            

          if(self.reconnecting == False):
               self.ui_window()
               print(self.reconnecting, "this is self.reconnecting")

     def ui_window(self):
          self.mainlabel = QLabel("Client login ")
          self.username = QLabel("Enter your username")
          self.textbox3 = QLineEdit(self)
          self.label2 = QLabel("Enter IP and port number to connect")
          self.textbox1 = QLineEdit(self)
          self.textbox1.setPlaceholderText("Type IP address")
          self.textbox2 = QLineEdit(self)
          self.textbox2.setPlaceholderText("Type Port number")
          self.button = QPushButton('Connect')
          self.button2 = QPushButton('Go back')
          self.layout = QVBoxLayout()
          self.layout.addWidget(self.username)
          self.layout.addWidget(self.textbox3)
          self.layout.addWidget(self.label2)
          self.layout.addWidget(self.textbox1)
          self.layout.addWidget(self.textbox2)
          self.layout.addWidget(self.button)
          #keyboard.on_press_key("Enter", lambda _: self.on_click()) //use later
          self.button.clicked.connect(self.on_click)

          self.setLayout(self.layout)    

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
               os.remove("temp-client.json")
               exit()
          else:
              pass
    
     def run_app(self):
          self.close()
          self.client = newWindow()
          self.client.show()
          
     def on_click(self):
          alert = QMessageBox()
          
        
          self.states.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
     
             
          if(self.states.client != None):
               print("does this get run?")
               exit()
                        
        
        
    
          if(os.path.exists("temp-client.json")):
               with open('temp-client.json', 'r') as output:
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
                         
                         self.states.s.connect((HOST, 12345)) 
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
               self.run_app()
            
            
               return   
            

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
               self.run_app()
               print("connected to server")
            

          except Exception:
               alert.setText("Wrong IP or port number! ")
               alert.setWindowTitle("Error")
               alert.setIcon(QMessageBox.Icon.Warning)
               alert.setStandardButtons(QMessageBox.StandardButton.Ok)
               alert.exec_()
            

    
         
     
class newWindow(QMainWindow):
     new_signal = pyqtSignal(str)
     def __init__(self):
            
          super().__init__()
          
          self.states = states
          
          self.handler = False
          
          self.new_signal.connect(self.update_label)

          self.thread = threading.Thread(target=self.receive, daemon = True)
          self.thread.start()
          
          self.ui_newWindow()
            
          

          
     def ui_newWindow(self):
          global navbar
          self.resize(1000,1000)
          self.setWindowTitle("Client app")
          navbar = self.menuBar()
          navbar.addMenu(self.states.username_input)
          self.status = navbar.addMenu(self.states.r)
          self.status.setStyleSheet("QMenuBar::indicator {color: red;}")
          self.central = QWidget()
          self.setCentralWidget(self.central)
          self.client = QVBoxLayout()
          self.message = QLineEdit(self)
          self.message.setGeometry(100, 500, 500, 100)
          self.button7 = QPushButton("Send",self)
          self.message.setPlaceholderText("Type in a message to send")
          self.button7.setGeometry(50, 50, 50, 50)
          self.button7.clicked.connect(lambda: self.send(self.message.text()))
            
            
          self.client.addWidget(self.message)
          self.client.addWidget(self.button7)
            
          self.button7.setStyleSheet("border-radius: 10px;")
          keyboard.on_press_key("Enter", lambda _: self.send(self.message.text()))

          self.new_signal.emit("far")
          self.central.setLayout(self.client)

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
                        
                         self.client.addWidget(self.label)
                    else:

                         print(msg)
                        
                         self.label = QLabel(username + ": "+ msg + " \n  " + time)
                         self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                         self.client.addWidget(self.label)
          else:
               print("fsagetg")
               for user, username, msg, time in self.states.messagesSent:
                        
                    if(user == "client"):
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
               self.states.r = "Server has disconnected. Attempting to reconnect."
               self.states.count = self.states.count + 1
          reconnected = False
          self.states.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          navbar.addMenu(self.states.r)
          for k in [1, 2, 4, 8, 12]:
               time.sleep(k)
                          
               try:
                    print(1)
                    self.states.s.connect((HOST, 12345))
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
          with open('temp-client.json', 'w') as output:
               if(os.path.getsize("temp-client.json")):
                  os.remove("temp-client.json")
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
                    os.remove("temp-client.json")
                    print("ooga booga?")
                    exit()
                     
               print("when does this get run?")
               json.dump(message_list, output, indent=4)
                                          
                                 
               output.close()

           
                 
           
     def receive(self):
        
          global data
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
                         
                     
                         
                
               
                
                
                
                
                
                
                
                
            
            

app = QApplication([])
window = window()
if(os.path.exists("temp-client.json")):
     pass
else:
     window.show()
app.exec()