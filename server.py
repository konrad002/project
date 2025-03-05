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
hostname = str(socket.gethostname())
HOST = socket.gethostbyname(hostname)

PORT = 12345
messagesSent = []
conn = None
pastConnections = {}
loading = False


                  
                  
            
                  
            


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
                              messagesSent.append((k["username"], k["message"], k["time"]))
                        print(r)
                        client_username = k["username"]
                        username = k["username"]
                        loading = True
                        
                        print("run?")
                        print(messagesSent)
                        output.close()
                        
                        
            elif(r == QMessageBox.Cancel):
                 os.remove("temp-server.json")
                 os.remove("temp-client.json")
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
            
            
            pastConnections["server"] = username
            pastConnections["client"] = client_username
            
            if(conn != None and len(pastConnections) > 2 ):
                  
                  print("error")
                  exit()
            

            elif(conn == None):
                 
                 print("how did we get here?")
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
            navbar = self.menuBar()

            self.new_signal.connect(self.update_label)
            
            thread2 = threading.Thread(target= self.receive, daemon = True)
            thread2.start()

            self.alert = QStatusBar()
            self.setStatusBar = (self.alert)
            self.alert.showMessage("Ready", 20000)

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
                  os.remove("temp-client.json")
           exit()
            
      
           
      def update_label(self): # TODO: Fix this awful code please. 1 loop is bad enough
                          
            global loading, client_username
            print(messagesSent)
            if(messagesSent != []):
                 pass
            
            if(loading == False):
                  for user, msg, time in messagesSent[-1:]:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
                        if(user == pastConnections["server"]):
                              print("run?, how many times?")
                        
                              self.label = QLabel(user + ": "+ msg + "  \n " + time)
                        
                              self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                              self.client.addWidget(self.label)
                        else:
                              print(msg)
                        
                              self.label = QLabel(user + ": "+ msg + " \n  " + time)
                              self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                              self.client.addWidget(self.label)
            else:
                 for user, msg, time in messagesSent:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
                        if(user == pastConnections["server"]):
                              print("run?, how many times?")
                        
                              self.label = QLabel(user + ": "+ msg + "  \n " + time)
                        
                              self.label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                              self.client.addWidget(self.label)
                        else:
                              print(msg)
                        
                              self.label = QLabel(user + ": "+ msg + " \n  " + time)
                              self.label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
                              self.client.addWidget(self.label)
                 loading = False

            
                  
           
            

      def send(self, message):
            if(message == ""):
                  return
            print(len(messagesSent))
            if(len(message) > 256):
                  print("Message is too long! Maximum length 256")
                  return
            global timeSent
            timeSent = datetime.now().strftime("%H:%M")
            messagesSent.append((username, message, timeSent))
            sending = {
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
           label2 = QMessageBox()
           label2.setText("Client has disconnected")
           label2.exec_()

           print("disconnected")
           with open('temp-server.json', 'w') as output:
            if(os.path.getsize("temp-server.json")):
                  os.remove("temp-server.json")
                  output.close()
            else:
                  message_list = []
                  for something in messagesSent:
                                          
                        sending = {
                         "username" : something[0],
                         "message" : something[1],
                         "time" : something[2]
                         }
                        message_list.append(sending)
                  json.dump(message_list, output, indent=4)
                                          
                  print(sending)
                                         
                  output.close()
            exit()        
      def receive(self):
            global conn, timeSent2, client_username
            
                 
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
                              QTimer.singleShot(0, self.disconnections)
                              break
                        print(data)
                        
                        
                        message = json.loads(data.decode("utf-8"))
                        print(message)
                        client_username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        messagesSent.append((client_username, message_received, timeSent2))
                        print(messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")
                              
                              
                        
                        
                        
                       
                        
           
      
      

            

            



app = QApplication([])
window = window()
window.show()

app.exec()





