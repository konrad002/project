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
       
class States:
      def __init__(self):
            self.s = None
            self.PORT = 12345
            self.messagesSent = []
            self.conn = None
            self.pastConnections = {}
            self.loading = False
            self.disconnected = False
            
            self.state0 = False
            self.check_state = None
            self.client_username = ""
            self.username = ""
            self.isReady = False
            self.client_socket = None 
            self.Dm = ""
           
            

states = States()

class Window(QWidget):
      def __init__(self):

            super().__init__()
      
            self.states = states
            self.reconnecting = False 
            
            
            
            self.thread = threading.Thread(target=self.connect, daemon = True)
            self.thread.start()
            self.active_windows = []
      
      
            
      
      

            if(os.path.exists("temp-server.json")):
                  self.reconnecting = True

            self.get_username()      
            
            if(not self.reconnecting):
                  self.ui_window()

      

      def ui_window(self):
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

      def set_username(self):  
            
            alert = QMessageBox()
            self.states.username, ok = QInputDialog.getText(self, "Enter your username", "Please enter your username")
            if(ok and self.states.username != ""):
                  print(self.states.username)
                  pass
            elif(ok and self.states.username == ""):
                  alert.setText("Please enter a username")
                  alert.exec_()
                  self.set_username()
            
      def get_username(self):
         
            
            print(self.thread.is_alive(), 3)
         
            if(os.path.exists("temp-server.json")):
            
                  label_username = QMessageBox()
                  label_username.setIcon(QMessageBox.Information)
                  label_username.setText("Want to relogin to past connection? 2")
                  label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                  r = label_username.exec_()
                  if(r == QMessageBox.Ok):
                   
                        with open('temp-server.json', 'r') as output:
                              r = json.load(output)
                              print(r)
                              self.states.client_username = r[0]["client_user"]
                              self.states.username = r[0]["server_user"] 
                              print(self.states.username, "this is username at line 123")
                              
                              f = r[1:len(r)]
                              for k in f:
                              
                                    self.states.messagesSent.append((k["user"], k["username"], k["message"], k["time"]))
                              print(r)
                        
                              self.states.loading = True
                        
                              print("run?")
                              print(self.states.messagesSent)
                              output.close()
                              self.states.state0 = True
                        print("surely this gets printed out no?")
                   
                        self.something()

                             
                  elif(r == QMessageBox.Cancel):
                        os.remove("temp-server.json")
                 
                        self.set_username()
                  else:
                        pass
         
            else:
                  self.set_username()
              
         
         
            
      def something(self):
            
            
         
         
         
            while(self.states.isReady == False):
            

                  print(self.states.isReady, "fhiasge")        
            
                  label4 = QMessageBox()
                  label4.setText("Waiting to reconnect... ")
                  label4.setStyleSheet("")
                             
                  label4.setWindowTitle(self.states.username + " " + "relogin?")
                  QTimer.singleShot(2000, label4.close)
                              
                  label4.exec_()
                  if(self.states.conn != None):
                        print("there is now a new connection")
                        self.states.isReady = True
                        
                        
                        return
                  if(self.thread.is_alive() == False):
                        print("running connect")
                        self.thread = threading.Thread(target=self.connect, daemon = True)
                        self.thread.start()
                  
                  print(self.thread.is_alive)
            
      
         
            
            
      def reuse(self):
            global navbar
            if(self.states.check_state != None):
                  print("xz")
                  navbar.clear()
                  navbar.addMenu(self.states.username)
                  
                  self.states.loading = None
            else:  
                  print("zx2", self.states.check_state)
                  self.states.check_state = 1
                  self.states.loading = True
                  QTimer.singleShot(0, self.show_window)

      def connect(self):
           
            
            print("are we even here?")
            print("are we here?")
          
      
            
      
            try:
                  self.states.s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
                  self.states.s.bind((HOST, self.states.PORT))
                  self.states.s.listen(1)
                  self.states.conn, self.states.addr = self.states.s.accept()
            except Exception as e:
                  print("j")
                  print(e)
                  exit()     
                  
      
      
                  
      
            
      

            print("connected now")
            while(self.states.state0 == False and self.reconnecting == True):
                  pass
            print(self.states.state0, self.reconnecting)
            if(os.path.exists("temp-server.json")):
                  
             
                  print("//??")
                  self.states.conn.sendall(b"ready")
                  print("s")
                  confirm = self.states.conn.recv(1024).decode()
                  print(confirm, "this is confirm")
                  if(confirm == "confirmed"):
                        z = True
                        while(z):
                              try: 
                                    self.states.pastConnections["client"] = self.states.client_username     
                                    self.states.pastConnections["server"] = self.states.username

                                    z = False
                                    print("username and client username have both been defined")
                              except:
                                    print("still waiting")
                        self.states.isReady = True
                        
                        self.reuse()
                        
                        
                        
                  
                        
            elif(os.path.exists("temp-server.json") == False):
                  self.states.isReady = True
                  print("fsf")
                  self.states.pastConnections["server"] = self.states.username
                  self.states.pastConnections["client"] = self.states.client_username
                  self.reuse()
      

    
      def show_window(self):
            
            print("was this even run?")
            self.close()
            self.states.client_socket = newWindow(self)
            self.states.client_socket.show()
            self.active_windows.append(self)
            
            
            print("connected to", self.states.addr)
            print(self.states.pastConnections, "line 163")
            print(self.active_windows)
            
    
              
class newWindow(QMainWindow):
      
      new_signal = pyqtSignal(str)  
      def __init__(self, instance):
            
            super().__init__()
            print("d")
            self.states = states
            
            self.instance = instance
            
            self.new_signal.connect(self.update_label)
            
            self.thread2 = threading.Thread(target= self.receive, daemon = True)
            self.thread2.start() 

            self.ui_newWindow()

            
            
                  
            
      def ui_newWindow(self):
            global navbar
            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            navbar = self.menuBar()
            navbar.addMenu(self.states.username)

            self.status = navbar.addMenu(self.states.Dm)
            self.status.setStyleSheet("QMenuBar::indicator {color: red;}")
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
<<<<<<< HEAD
            central.setLayout(self.client)

=======
>>>>>>> testing
            
            self.new_signal.emit("fa")
            
                  
            central.setLayout(self.client)           
      def call_window(self):
            self.instance.connect()
      
      def closeEvent(self, event):
            print("z2")
            self.parse_temp()  
            event.accept()

      

            
      
      
         
      def update_label(self): # TODO: Fix this awful code please. 1 loop is bad enough
                          
            
            print(self.states.messagesSent)
            print("run during here?", self.states.loading)
            if(self.states.messagesSent != []):
                 pass
            
            if(self.states.loading == False):
                  for user, username, msg, time in self.states.messagesSent[-1:]:
                        print(msg)
                        print(user)
                  
            
                        print(self.states.loading)
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
            elif(self.states.loading == True):
                  for user, username, msg, time in self.states.messagesSent:
                  
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
                  self.states.loading = False
            else:
                  self.states.loading = False
                 
            
                  
           
            
      
            
      def send(self, message):
            
            if(message == ""):
                  return
            print(len(self.states.messagesSent))
            if(len(message) > 256):
                  alert3 = QMessageBox()
                  alert3.setText("Message is too long.\n Maximum length is 256.")
                  alert3.exec_()
                  self.message.setText("")
                  return
            
            
            timeSent = datetime.now().strftime("%H:%M")
            self.states.messagesSent.append(("server", self.states.username, message, timeSent))
            sending = {
             "user" : "server",
             "username" : self.states.username,
             "message" : message,
             "time" : timeSent
            }

            print(timeSent)
            
            data = json.dumps(sending)
            print(data, "this is data yet again")
            self.states.conn.sendall(data.encode("utf-8"))
            print(self.states.messagesSent)
            self.message.setText("")
            
            self.states.loading = False
            
            self.new_signal.emit(message)

      def trying(self):

            if(self.thread2.is_alive() == False):
                  
                  self.thread2 = threading.Thread(target= self.receive, daemon = True)
                  self.thread2.start()        

      def disconnections(self):
           
            global navbar
            self.states.conn = None
            print("disconnections called how many times?")
           
            self.states.Dm = "Client has disconnected. Attempting to reconnect."
            navbar.setStyleSheet("QMenuBar::indicator {color: red;}")
            self.states.isReady = False
            reconnected = False
            
            self.thread = threading.Thread(target=self.states.client_socket.call_window, daemon = True)
            self.thread.start()
            navbar.addMenu(self.states.Dm)
           
            for k in [1, 2, 4, 8, 12]:
                  time.sleep(k)
                  print(self.thread.is_alive(), 1)
                  if(self.states.isReady):
                        reconnected = True
                        break
                  try:
                        
                        print(3)
                        self.states.conn.sendall(b"ready")
                        print(4)
                        reconnected = True
                        break
                              
                  except:
                        print("exception")

            if(not reconnected):
                  print("7")
                  exit()
            print(reconnected)          
            reconnected = False  
            
                     
             
            print("done")
            
            
                  
                  
            self.states.loading = False
            self.trying()
            print(self.thread2.is_alive)
            

      def parse_temp(self):
                
            with open('temp-server.json', 'w') as output:
                  if(os.path.getsize("temp-server.json")):
                        os.remove("temp-server.json")
                        output.close()
           
                 
                  else:
                  
                  
                  
                        message_list = []
                        sending = {
                              "client_user": self.states.client_username,
                              "server_user" : self.states.username
                        }
                        self.states.pastConnections["client"] = sending["client_user"]
                        self.states.pastConnections["server"] = sending["server_user"]
                        message_list.append(sending)
                        
                        for something in self.states.messagesSent:
                                          
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
                       
                              exit()
                        print("when does this get run?")
                        json.dump(message_list, output, indent=4)
                                          
                        print(sending)
                                         
                        output.close()

           
           
           
                
           
           
                  
           
      def receive(self):
 
          global data 
          while True:
                  

                  ready, _, _ = select.select([self.states.conn], [], [], 0.5)
                  

                  print(ready, "this is ready")
                        
                  if(ready):
                        
                        try:
                              
                                   
                              data = self.states.conn.recv(1024)
                              if(not data):
                                   print("client has disconnected.")
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
                        self.states.client_username = message["username"]
                        message_received = message["message"]
                        timeSent2 = message["time"]
                        self.states.messagesSent.append((user, self.states.client_username, message_received, timeSent2))
                        print(self.states.messagesSent)
                        self.new_signal.emit(message_received)
                        print("what about this?")
                              
                              
                        
       

app = QApplication([])
window = Window()
if(os.path.exists("temp-server.json")):
     pass
else:
     window.show()

app.exec()





