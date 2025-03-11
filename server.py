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
hostname = str(socket.gethostname())
HOST = socket.gethostbyname(hostname)

PORT = 12345
messagesSent = []
conn = None
pastConnections = {}
loading = False
disconnected_from_receive = False

                  
                  
            
                  
            


class window(QWidget):
    def __init__(self):
     
      super().__init__()
      
      self.client_socket = None
      thread = threading.Thread(target=self.connect, daemon = True)
      thread.start()
      global client_username
      client_username = None
      
      
      self.get_username()
      print("rsaf")
      self.resize(1000, 1000)
      self.setWindowTitle("Please wait for connection")
      
      self.label17 = QLabel("Please wait for client to connect")
      self.ip = QLabel("Connect to this IP!")
      self.ip2 = QLabel(HOST)
      self.ip2.setFont(QFont('Montserrat', 20))
        
      self.ip.setFont(QFont('Arial', 20))
      self.label17.move(200,200)
      self.label17.setFont(QFont('Arial', 20))
      
      self.image = QLabel(self)
      pixelmap = QPixmap("pic.webp")
      self.label19 = QLabel(self)
      self.image.setPixmap(pixelmap)

      

      self.layout = QVBoxLayout()
      self.layout.addWidget(self.label17)
      self.label17.setAlignment(Qt.AlignCenter)
      self.layout.addWidget(self.ip)
      self.ip.setAlignment(Qt.AlignCenter)
      self.layout.addWidget(self.ip2)
      self.ip2.setAlignment(Qt.AlignCenter)
      
      self.layout.addWidget(self.image)
      self.image.setScaledContents(True)
      print("fas2")
      self.setLayout(self.layout)
       
      print("fas")
    def set_username(self):  
         global username
         alert = QMessageBox()
         username, ok = QInputDialog.getText(self, "Enter your username", "Please enter your username")
         if(ok and username != ""):
            print(username)
            pass
         elif(ok and username == ""):
            alert.setText("Please enter a username")
            alert.exec_()
            self.set_username()
    def get_username(self):
         
         global username, s, client_username, loading
         
         if(os.path.exists("temp-server.json")):
            
            label_username = QMessageBox()
            label_username.setIcon(QMessageBox.Information)
            label_username.setText("Want to relogin to past connection?")
            label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            r = label_username.exec_()
            if(r == QMessageBox.Ok):
                   
                   with open('temp-server.json', 'r') as output:
                        r = json.load(output)
                        
                        for k in r:
                              
                              messagesSent.append((k["user"], k["username"], k["message"], k["time"]))
                        print(r)
                        
                        loading = True
                        
                        print("run?")
                        print(messagesSent)
                        output.close()
                   with open("temp-username.json", "r") as read:
                        r2 = json.load(read)
                        client_username = r2["client_user"]
                        username = r2["server_user"]
                        read.close()
                   print("surely this gets printed out no?")
                   while True:
                        if(conn == None):
                              label4 = QMessageBox()
                              label4.setText("Waiting to reconnect... ")
                              label4.setStyleSheet("")
                              QTimer.singleShot(3000, label4.close)
                              if(os.path.exists("temp-server.json") == False):
                                   return
                              label4.exec_()
                              
                        else:
                            
                             return
                             
            elif(r == QMessageBox.Cancel):
                 os.remove("temp-server.json")
                 os.remove("temp-username.json")
                 self.set_username()
            else:
                 pass
         
         else:
            self.set_username()
              
         
         
            
            
    
    def connect(self):

      print("are we even here?")
      print("are we here?")
            
      
      global s, conn, addr, client_username, username
      s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
      s.bind((HOST, PORT))
      s.listen(2)
            
      
      
                  
      while True:
             
            conn, addr = s.accept()
            
            
            print("j")
            pastConnections["server"] = username
            pastConnections["client"] = client_username
            
                      
                 
            if(conn != None and len(pastConnections) > 2 ):
                  
                  print("error")
                  exit()
            

            elif(conn == None):
                 
                  print("Still waiting for client to reconnect.")
                  s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
                  s.bind((HOST, PORT))
                      
                  s.listen(2)
                  conn, addr = s.accept()
                  print(conn, addr)
                  if(s.fileno() != -1):
                       print("Client has reconnected.")
            elif(conn != None):
                 QTimer.singleShot(0, self.show_window)
            
            

              

            
            print(pastConnections)

    def show_window(self):
         
         self.close()
         self.client_socket = newWindow()
         self.client_socket.show()
         print("connected to", addr)
         print(pastConnections, "line 163")
    
    
              
class newWindow(QMainWindow):
      
      new_signal = pyqtSignal(str)  
      def __init__(self):
            super().__init__()
            
            print("here")
            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            self.navbar = self.menuBar()
            
            
            
            self.navbar.addMenu(username)

            
            
            r = ""
            self.status = self.navbar.addMenu(r)
            self.status.setStyleSheet("QMenuBar::indicator {color: red;}")
            
            self.new_signal.connect(self.update_label)
            
            thread2 = threading.Thread(target= self.receive, daemon = True)
            thread2.start() 

           

            central = QWidget()
            self.setCentralWidget(central)
            self.client = QVBoxLayout()
            self.message = QLineEdit(self)
            
            self.button7 = QPushButton("Send",self)
            self.message.setPlaceholderText("Type in a message to send")
            self.button7.setGeometry(50, 50, 50, 50)
            self.button7.clicked.connect(lambda: self.send(self.message.text()))
            self.exit = QPushButton("End", self)
            self.exit.setGeometry(50, 50, 50, 50)
            self.exit.clicked.connect(lambda: self.exitConnection())
            
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            self.client.addWidget(self.exit)
            self.button7.setStyleSheet("border-radius: 10px;")
            keyboard.on_press_key("Enter", lambda _: self.send(self.message.text()))
            
            self.new_signal.emit("fa")
            
                  
            central.setLayout(self.client)
            
            
      def closeEvent(self, event):
           self.disconnections()  
           event.accept()

      def exitConnection(self):
           conn.close()
           if(os.path.exists("temp-server.json")):
                  os.remove("temp-server.json")
                  os.remove("temp-username.json")
                 
           exit()
            
      
           
      def update_label(self): # TODO: Fix this awful code please. 1 loop is bad enough
                          
            global loading, client_username
            print(messagesSent)
            if(messagesSent != []):
                 pass
            
            if(loading == False):
                  for user, username, msg, time in messagesSent[-1:]:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
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
            else:
                 for user, username, msg, time in messagesSent:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
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
                 loading = False

            
                  
           
            

      def send(self, message):
            if(message == ""):
                  return
            print(len(messagesSent))
            if(len(message) > 256):
                  alert3 = QMessageBox()
                  alert3.setText("Message is too long.\n Maximum length is 256.")
                  alert3.exec_()
                  self.message.setText("")
                  return
            
            global timeSent
            timeSent = datetime.now().strftime("%H:%M")
            messagesSent.append(("server", username, message, timeSent))
            sending = {
             "user" : "server",
             "username" : username,
             "message" : message,
             "time" : timeSent
            }

            print(timeSent)
            data = json.dumps(sending)
            conn.sendall(data.encode("utf-8"))
            print(messagesSent)
            self.message.setText("")
            self.new_signal.emit(message)
            
      def disconnections(self):
           global s,conn, r
           if(disconnected_from_receive):
                
                self.timer = QTimer() #TODO fix this
                
                r = "Client has disconnected. Attempting to reconnect."
                
                self.navbar.addMenu(r)
                

           print("disconnected")
           with open('temp-server.json', 'w') as output:
            if(os.path.getsize("temp-server.json")):
                  os.remove("temp-server.json")
                  output.close()
           
                 
            else:
                  message_list = []
                  for something in messagesSent:
                                          
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
                       os.remove("temp-server.json")
                       os.remove("temp-username.json")
                       exit()
                  print("when does this get run?")
                  json.dump(message_list, output, indent=4)
                                          
                  print(sending)
                                         
                  output.close()
           with open("temp-username.json", "w") as username_output:
                  
                  sending = {
                       "client_user": client_username,
                       "server_user" : username
                  }
                  pastConnections["client"] = sending["client_user"]
                  pastConnections["server"] = sending["server_user"]
                  json.dump(sending, username_output)
                  username_output.close()
                  
           
      def receive(self):
            global conn, timeSent2, client_username, disconnected_from_receive
            
                 
            while True:
                  

                  ready, _, _ = select.select([conn], [], [], 0.5)
                 
                        
                  if(ready):
                        if(conn == None):
                             print("does this get run? here?")
                             break
                        try:
                              data = conn.recv(1024)
                              print("this has been run")
                        except:
                              disconnected_from_receive = True
                              QTimer.singleShot(0, self.disconnections)
                              
                              
                              break
                        print(data)
                        
                        
                        message = json.loads(data.decode("utf-8"))
                        print(message)
                        user = message["user"]
                        client_username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        messagesSent.append((user, client_username, message_received, timeSent2))
                        print(messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")
                              
                              
                        
                        
                        
                       
                        
           
      
      

            

            



app = QApplication([])
window = window()
window.show()

app.exec()





