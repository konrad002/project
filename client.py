import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import *
import keyboard
import json
from datetime import datetime, timedelta
messagesSent = []
pastConnections = {}
import os
import time
import sys
loading = False
disconnected_from_receive = False
disconnected = False
s = None

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        
        global client_username
        client_username = None
        
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
        if(os.path.exists("temp-client.json")):
            self.rr()

        
    def rr(self):
         
         
         label_username = QMessageBox()
         label_username.setIcon(QMessageBox.Information)
         label_username.setText("Want to relogin to past connection?")
         label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
         r = label_username.exec_()
         if(r == QMessageBox.Ok):
              self.on_click(False)
              return
         elif(r == QMessageBox.Cancel):
              os.remove("temp-client.json")
              
              exit()
         else:
              pass
    def on_click(self, isReady):
        alert = QMessageBox()
        global s, username_input, client_username, loading, disconnected
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.client != None):
                    print("does this get run?")
                    
                    exit()
                        
        
        
    
        if(os.path.exists("temp-client.json")):
            with open('temp-client.json', 'r') as output:
                r = json.load(output)
                username_input = r[0]["client_user"]
                client_username = r[0]["server_user"]   
                disconnected = r[1]["disconnected"]
                f = r[2:len(r)]     
                for k in f:
                    
                    messagesSent.append((k["user"], k["username"], k["message"], k["time"]))


                print(r)
                
                
                
                loading = True
                print("run?")
                print(messagesSent)
                output.close()
            
            hostname = str(socket.gethostname())
            HOST = socket.gethostbyname(hostname)
            
            
            while True: #TODO
                
                if(s.connect_ex((HOST, 12345)) != 0 and isReady == False):
                    label4 = QMessageBox()
                    label4.setText("Waiting to reconnect... 2 ")
                    label4.setStyleSheet("")
                    
                    label4.setWindowTitle(username_input + " "+ "relogin?")
                    
                    QTimer.singleShot(3000, label4.close)
                    label4.exec_()  
                    print(s.fileno(), "gsgwe")
                    print(isReady)
                    try:
                         data = s.recv(1024).decode()
                         if(data == "ready"):
                              isReady = True
                    except:
                         pass
                elif(isReady == True): 
                    s.sendall(b"confirmed")
                    
                    break
                
            print("do we ever get here?")             
            
            
            
            self.close()
            self.hide()
            self.client = newWindow()
            self.client.show()
            
            
            return   
            

        try:
            
            print("???")
            
            s.connect((self.textbox1.text(), int(self.textbox2.text())))
            
            
            print(pastConnections)
            username_input = self.textbox3.text()
            pastConnections["user"] = "client"
            pastConnections["client"] = username_input
            pastConnections["server"] = client_username
            print(username_input, client_username)
            if(username_input == client_username):
                 print("client and server username's are the same!!!!")
            self.close()
            self.client = newWindow()
            self.client.show()
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
            self.resize(1000,1000)
            self.setWindowTitle("Client app")
            self.navbar = self.menuBar()
            
            
            self.navbar.addMenu(username_input)
            global r
            r = ""
            self.status = self.navbar.addMenu(r)
            self.status.setStyleSheet("QMenuBar::indicator {color: red;}")
            
            self.new_signal.connect(self.update_label)

            thread = threading.Thread(target=self.receive, daemon = True)
            thread.start()

            central = QWidget()
            self.setCentralWidget(central)
            self.client = QVBoxLayout()
            self.message = QLineEdit(self)
            self.message.setGeometry(100, 500, 500, 100)
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
            keyboard.on_press_key("Enter", lambda _: self.send(self.message.text()))#
            self.new_signal.emit("far")
            central.setLayout(self.client)

      def closeEvent(self, event):
           self.disconnections()  
           event.accept()     

      def exitConnection(self):
           s.close()
           if(os.path.exists("temp-client.json")):
                  os.remove("temp-client.json")
                  
                  
           exit()
      def update_label(self): #TODO: Fix this god awful code.
                       
            global client_username, loading
            print(messagesSent, "fsagf")       
            
            if(loading == False):
                  for user, username, msg, time in messagesSent[-1:]:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
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
                 for user, username, msg, time in messagesSent:
                        print(msg)
                        print(user)
                  
            
                        print(loading)
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
                 loading = False
            
                    
                    
                    
                    
                

            
            
      def send(self, message):
        if(message == ""):
            return
        if(len(message) > 256):
            alert3 = QMessageBox()
            alert3.setText("Message is too long.\n\nMaximum length is 256.")
            alert3.exec_()
            self.message.setText("")
            return
        
        print(len(messagesSent))
        global timeSent
        timeSent = datetime.now().strftime("%H:%M")
        
        
        alert = QMessageBox()
        
        #for i, j, k in messagesSent:
        #    userSecond = datetime.strptime(k, "%H:%M:%S")
        #    print(userSecond, new)
        #    if(new >= userSecond and len(messagesSent) >1):
        #        alert.setText("Sending too fast")
        #        alert.exec_()
        #        message = ""
                

        messagesSent.append(("client", username_input, message, timeSent))
        sending = {
             "user": "client",
             "username" : username_input,
             "message" : message,
             "time": timeSent
        }
        
        
        data = json.dumps(sending)
        s.sendall(data.encode("utf-8"))
                

        
        print("does this get run here?")
        print(messagesSent)
        self.message.setText("")
        self.new_signal.emit(message)  
        
      def disconnections(self):
           global r
           disconnected = True
           if(disconnected_from_receive and s.fileno() == -1):
                r = "Server has disconnected. Attempting to reconnect."
                
                self.navbar.addMenu(r)

           with open('temp-client.json', 'w') as output:
                if(os.path.getsize("temp-client.json")):
                  os.remove("temp-client.json")
                  output.close()
                message_list = []
                sending = {
                       "client_user": username_input,
                       "server_user" : client_username
                  }
                pastConnections["client"] = sending["client_user"]
                pastConnections["server"] = sending["server_user"]
                message_list.append(sending)
                sending = {
                     "disconnected" : disconnected
                }
                message_list.append(sending)

                for something in messagesSent:
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

           py = sys.executable
           os.execv(py, [py] + sys.argv)
                 
           
      def receive(self):
        
        global client_username, timeSent2, data, disconnected_from_receive
        while True:
            
            ready, _, _ = select.select([s], [], [], 0.5)
            print(ready)
            
            if(ready):
                
                     
                try:
                    data = s.recv(1024)
                    print(data)
                    
                except:
                     disconnected_from_receive = True
                     self.disconnections()
                     break
                
                message = json.loads(data.decode("utf-8"))
                print(message)
                user = message["user"]
                client_username = message["username"]
                message_received = message["message"]
                timeSent2 = message["time"]
                
                messagesSent.append((user, client_username, message_received, timeSent2))
                print(messagesSent)
                self.new_signal.emit(message_received)
                
                
                
                
                
                
                
                
            
            

app = QApplication([])
window = window()
window.show()
app.exec()