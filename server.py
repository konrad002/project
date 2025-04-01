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
disconnected = False
total_users = 0   
state0 = False               
check_state = None          
                  
            


class Window(QWidget):
      def __init__(self):

            super().__init__()
      
            global client_username, check_state
            self.reconnecting = False
            self.client_socket = None
            client_username = None
            check_state = None
            self.thread = threading.Thread(target=self.connect, daemon = True)
            self.thread.start()
            self.active_windows = []
      
      
            self.get_username()
      
      

            if(os.path.exists("temp-server.json")):
                  self.reconnecting = True
                  self.close()
            
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
         
            global username, s, client_username, loading, total_users, state0
            print(self.thread.is_alive(), 3)
         
            if(os.path.exists("temp-server.json")):
            
                  label_username = QMessageBox()
                  label_username.setIcon(QMessageBox.Information)
                  label_username.setText("Want to relogin to past connection? 2")
                  label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                  r = label_username.exec_()
                  if(r == QMessageBox.Ok):
                   
<<<<<<< HEAD
                        with open('temp-server.json', 'r') as output:
                              r = json.load(output)
                              print(r)
                              client_username = r[0]["client_user"]
                              username = r[0]["server_user"] 
                              print(username, "this is username at line 123")
                              total_users = r[1]["total_users"]
                              f = r[2:len(r)]
                              for k in f:
=======
                   with open('temp-server.json', 'r') as output:
                        r = json.load(output)
                        print(r)
                        client_username = r[0]["client_user"]
                        username = r[0]["server_user"] 
                        print(username, "this is username at line 123")
                        total_users = r[1]["total_users"]
                        f = r[2:len(r)]
                        for k in f:
>>>>>>> 12f875f05d771e6f8bb11142876ffebaefd8430b
                              
                                    messagesSent.append((k["user"], k["username"], k["message"], k["time"]))
                              print(r)
                        
                              loading = True
                        
<<<<<<< HEAD
                              print("run?")
                              print(messagesSent)
                              output.close()
                              state0 = True
                        print("surely this gets printed out no?")
                   
                        self.something()
=======
                        print("run?")
                        print(messagesSent)
                        output.close()
                        state0 = True
                   print("surely this gets printed out no?")
                   
                   self.something()
>>>>>>> 12f875f05d771e6f8bb11142876ffebaefd8430b

                             
                  elif(r == QMessageBox.Cancel):
                        os.remove("temp-server.json")
                 
                        self.set_username()
                  else:
                        pass
         
            else:
                  self.set_username()
              
         
         
            
      def something(self):
            global isReady
            isReady = False  
         
         
         
            while(isReady == False):
            

                  print(isReady, "fhiasge")        
            
                  label4 = QMessageBox()
                  label4.setText("Waiting to reconnect... ")
                  label4.setStyleSheet("")
                             
                  label4.setWindowTitle(username + " " + "relogin?")
                  QTimer.singleShot(2000, label4.close)
                              
                  label4.exec_()
                  if(conn != None):
                        print("there is already a connection")
                        isReady = True
                        return
                  if(self.thread.is_alive() == False):
                        print("running connect")
                        self.thread = threading.Thread(target=self.connect, daemon = True)
                        self.thread.start()
                  
                  print(self.thread.is_alive)
            
      
         
            
            
      def reuse(self):
            global loading, check_state
            if(check_state != None):
                  print("xz")
                  navbar.clear()
                  navbar.addMenu(username)
                  loading = None
            else:  
                  print("zx2")
                  check_state = 1
                  QTimer.singleShot(0, self.show_window)
      def connect(self):
            global s, conn, addr, client_username, username, total_users, isReady, sgf, loading
            count = 0
            print("are we even here?")
            print("are we here?")
          
      
            
      
            try:
                  s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
                  s.bind((HOST, PORT))
                  s.listen(1)
                  conn, addr = s.accept()
            except Exception as e:
                  print("j")
                  print(e)
                  exit()     
                  
      
      
                  
      
            
      

            print("connected now")
            while(state0 == False and self.reconnecting == True):
                  pass
      
            if(os.path.exists("temp-server.json")):
                  
             
<<<<<<< HEAD
                  print("//??")
                  conn.sendall(b"ready")
                  print("s")
                  confirm = conn.recv(1024).decode()
                  print(confirm, "this is confirm")
                  if(confirm == "confirmed"):
                        z = True
                        while(z):
                              try: 
                                    pastConnections["client"] = client_username     
                                    pastConnections["server"] = username
                         
                                    z = False
                                    print("username and client username have both been defined")
                              except:
                                    pass
                        isReady = True
                        self.reuse()
=======
            print("//??")
            conn.sendall(b"ready")
            print("s")
            confirm = conn.recv(1024).decode()
            print(confirm, "this is confirm")
            if(confirm == "confirmed"):
                  z = False
                  while(z):
                    try:      
                         pastConnections["server"] = username
                         pastConnections["client"] = client_username
                         z = False
                         print("username and client username have both been defined")
                    except:
                         pass
                  isReady = True
                  if(sgf != None):
                       print("xz")
                       navbar.clear()
                       navbar.addMenu(username)
                       loading = None
                  else:  
                    print("zx2")
                    sgf = 1
                    QTimer.singleShot(0, self.show_window)
>>>>>>> 12f875f05d771e6f8bb11142876ffebaefd8430b
                        
                        
                        
                  
                        
<<<<<<< HEAD
            elif(os.path.exists("temp-server.json") == False):
                  isReady = True
                  print("fsf")
                  pastConnections["server"] = username
                  pastConnections["client"] = client_username
                  self.reuse()
=======
      elif(os.path.exists("temp-server.json") == False):
            isReady = True
            print("fsf")
            pastConnections["server"] = username
            pastConnections["client"] = client_username
            if(sgf != None):
               print("xz")
               navbar.clear()
               navbar.addMenu(username)
               loading = None
            else:  
               print("zx2")
               sgf = 1
               QTimer.singleShot(0, self.show_window)
>>>>>>> 12f875f05d771e6f8bb11142876ffebaefd8430b
      

    
      def show_window(self):
            global client_socket
            print("was this even run?")
            self.close()
            self.client_socket = newWindow(self)
            self.client_socket.show()
            self.active_windows.append(self)
            
            client_socket = self.client_socket
            print("connected to", addr)
            print(pastConnections, "line 163")
            print(self.active_windows)
            
    
              
class newWindow(QMainWindow):
      
      new_signal = pyqtSignal(str)  
      def __init__(self, instance):
            global r, navbar
            super().__init__()
            
            r = ""
            self.instance = instance
            
            self.new_signal.connect(self.update_label)
            
            thread2 = threading.Thread(target= self.receive, daemon = True)
            thread2.start() 

            self.ui_newWindow()

            
            
                  
            
      def ui_newWindow(self):
            global navbar
            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            navbar = self.menuBar()
            navbar.addMenu(username)

            self.status = navbar.addMenu(r)
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
            
            self.new_signal.emit("fa")
            
                  
            central.setLayout(self.client)           
      def call_window(self):
            self.instance.connect()
      
      def closeEvent(self, event):
            print("z2")
            self.parse_temp()  
            event.accept()

      

            
      
      
         
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
            elif(loading == True):
                  for user, username, msg, time in messagesSent:
                  
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
            else:
                  loading = False
                 
            
                  
           
            

      def send(self, message):
            global timeSent
            if(message == ""):
                  return
            print(len(messagesSent))
            if(len(message) > 256):
                  alert3 = QMessageBox()
                  alert3.setText("Message is too long.\n Maximum length is 256.")
                  alert3.exec_()
                  self.message.setText("")
                  return
            
            
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
            print(data, "this is data yet again")
            conn.sendall(data.encode("utf-8"))
            print(messagesSent)
            self.message.setText("")
            self.new_signal.emit(message)

            

      def disconnections(self):
           
            global r, loading, navbar
            print("disconnections called how many times?")
           
            r = "Client has disconnected. Attempting to reconnect."

            reconnected = False
            self.thread = threading.Thread(target=client_socket.call_window, daemon = True)
            self.thread.start()
            navbar.addMenu(r)
           
            for k in [1, 2, 4, 8, 12]:
                  time.sleep(k)
                  print(self.thread.is_alive(), 1)
                  if(isReady):
                        reconnected = True
                        break
                  try:

                        print(3)
                        conn.sendall(b"ready")
                        print(4)
                        reconnected = True
                        break
                              
                  except:
                        print("exception")

            if(not reconnected):
                  exit()
                    
               
           
                     
                
            print("done")
            loading = True

      def parse_temp(self):
                
            with open('temp-server.json', 'w') as output:
                  if(os.path.getsize("temp-server.json")):
                        os.remove("temp-server.json")
                        output.close()
           
                 
                  else:
                  
                  
                  
                        message_list = []
                        sending = {
                              "client_user": client_username,
                              "server_user" : username
                        }
                        pastConnections["client"] = sending["client_user"]
                        pastConnections["server"] = sending["server_user"]
                        message_list.append(sending)
                        sending = {
                              "total_users" : total_users
                        }
                        message_list.append(sending)
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
                       
                              exit()
                        print("when does this get run?")
                        json.dump(message_list, output, indent=4)
                                          
                        print(sending)
                                         
                        output.close()

           
           
           
                
           
           
                  
           
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
                              if(not data):
                                   print("client has disconnected.")
                                   return
                              print(data, "this is data")
                              print("this has been run")
                        except Exception as e:
                              print(e)
                              print("z?")
                              print(e)
                              disconnected_from_receive = True
                              QTimer.singleShot(0, self.parse_temp)
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
window = Window()
if(os.path.exists("temp-server.json")):
     pass
else:
     window.show()

app.exec()





