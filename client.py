import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import pyqtSignal
import keyboard
import json
from datetime import datetime
messagesSent = []


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        
        
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

        

    def on_click(self):
        alert = QMessageBox()
        global s, username_input

        
        if(self.client != None):
                    print("does this get run?")
                    
                    exit()
                        
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            
        try:
            s.connect((self.textbox1.text(), int(self.textbox2.text())))
            username_input = self.textbox3.text()
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
            navbar = self.menuBar()
            self.label19 = QLabel("Client messenger ")
            
            navbar.addMenu(username_input)
            exit = QAction("Exit", self)
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
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            self.button7.setStyleSheet("border-radius: 10px;")
            keyboard.on_press_key("Enter", lambda _: self.send(self.message.text()))
            central.setLayout(self.client)
            
      def update_label(self, message):
                       
            print(message)
                    
            for user, msg in messagesSent:
                if(user == "User 1"):
                            
                    message_layout = QHBoxLayout()
                    label = QLabel(client_username + ": " + message + " \n " + timeSent2)
                    label.setWordWrap(True)
                    label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                    message_layout.addStretch()
                    
                elif(user == "User 2"):
                        message_layout = QHBoxLayout()
                        label = QLabel(username_input + ": "+ message +" \n  " +timeSent)
                        label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
            
            self.client.addWidget(label)
                    
                    
                    
                    
                

            
            
      def send(self, message):
        if(message == ""):
            return
        if(len(message) > 256):
            print("Message is too long! Maximum length 256")
            return
        print(len(messagesSent))
        global timeSent
        timeSent = datetime.now().strftime("%H:%M")

        messagesSent.append(("User 2", message))
        sending = {
             "username" : username_input,
             "message" : message,
             "time": timeSent
        }
        
        
        data = json.dumps(sending)
        s.sendall(data.encode("utf-8"))
                

        print(message, 2421841)
        print(s.getsockname())
        print("does this get run here?")
        print(messagesSent)
        self.message.setText("")
        self.new_signal.emit(message)  
        

      def receive(self):
        global client_username, timeSent2
        while True:
            ready, _, _ = select.select([s], [], [], 0.5)
            print(ready)
            if(ready):
                data = s.recv(1024)

                if(not data):
                    print("disconnected")
                    app.exit()
                    break
                
                message = json.loads(data.decode("utf-8"))
                print(message)
                client_username = message["username"]
                message_received = message["message"]
                timeSent2 = message["time"]
                
                messagesSent.append(("User 1", message_received))
                print(messagesSent)
                self.new_signal.emit(message_received)
                        
            

app = QApplication([])
window = window()
window.show()
app.exec()