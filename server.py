import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import select
import keyboard
import json
from datetime import datetime

hostname = str(socket.gethostname())
HOST = socket.gethostbyname(hostname)

PORT = 12345
messagesSent = []
conn = None
pastConnections = []

def connect():

      print("are we even here?")
      print("are we here?")
            
      global s, conn
            
      s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
      s.bind((HOST, PORT))
      s.listen(2)
            
            
      while True:
                  
            conn, addr = s.accept()
            print(conn)
            pastConnections.append(addr)
            if(conn != None and len(pastConnections) > 1 ):
                  print("error")
                  s.close()
                  s.__exit__()
                  app.exit()

                  exit()
            elif(conn == None):
                 print("does this ever get run?")
                 exit()

            print("connected to", addr)
            print(pastConnections)
                  
                  
            
                  
            


class window(QWidget):
    def __init__(self):
        
      super().__init__()
      self.client_socket = None
      self.username = self.get_username()  
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
      
      self.setLayout(self.layout)
      
        
    def get_username(self):
          global username
          username, ok = QInputDialog.getText(self, "Enter your username", "Please enter your username")
          if(ok and username != ""):
            
            self.check_connection(username)
            return
          elif(ok and username == ""):
            print("enter username")
            
            self.get_username()
          else:
               print("fhasfgsa")
               exit()
               
               
          
          
    def check_connection(self, username):
      
      print(username, "line 65")
      
      if(conn == None and username != ""):
                    
            print("Please wait for client to connect", 3000)
            
            while True:
                  if(conn != None):
                        
                        self.close()
                        self.client_socket = newWindow()
                        self.client_socket.show()
                        break
      else:
           exit()

              
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
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            self.button7.setStyleSheet("border-radius: 10px;")
            keyboard.on_press_key("Enter", lambda _: self.send(self.message.text()))
            central.setLayout(self.client)
            
            
           
            
      def update_label(self, message):
                          
            print(message)
            for user, msg in messagesSent:
                  if(user == "User 2"):
                        
                        label = QLabel(client_username + ": "+ message + "  \n " + timeSent2)

                        label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                        
                  elif(user == "User 1"):
                        
                        label = QLabel(username + ": "+ message + " \n  " + timeSent)
                        label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                        
            self.client.addWidget(label)
                    

      def send(self, message):
            if(message == ""):
                  return
            print(len(messagesSent))
            if(len(message) > 256):
                  print("Message is too long! Maximum length 256")
                  return
            global timeSent
            timeSent = datetime.now().strftime("%H:%M")
            messagesSent.append(("User 1", message))
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
            
            
      def receive(self):
            global conn, client_username, timeSent2

            while True:
                  if conn == None:
                        continue

                  ready, _, _ = select.select([conn], [], [], 0.5)
                  print(ready, "line 119")
                        
                  if(ready):
                        data = conn.recv(1024)
                        print("this has been run")
                        if(not data):
                              print("disconnected")
                              break
                        print(data)
                        
                        message = json.loads(data.decode("utf-8"))
                        print(message)
                        client_username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        messagesSent.append(("User 2", message_received))
                        print(messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")
           
      
      

            

            

thread = threading.Thread(target=connect, daemon = True)
thread.start()

app = QApplication([])
window = window()
window.show()

app.exec()





