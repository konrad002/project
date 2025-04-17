from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import keyboard
from datetime import datetime
from src_server.states import *
import json
import bcrypt
import select
from src_server.disconnect import parse_temp, disconnections




def ui_newWindow(self):
            
            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            self.states.navbar = self.menuBar()
            self.states.navbar.addMenu(self.states.username)

            
            self.states.navbar.setStyleSheet("color: blue;")
            central = QWidget()
            self.setCentralWidget(central)
            self.client = QVBoxLayout()
            self.message = QLineEdit(self)
            
            self.button7 = QPushButton("Send",self)
            self.message.setPlaceholderText("Type in a message to send")
            self.button7.setGeometry(50, 50, 50, 50)
            self.button7.clicked.connect(lambda: send(self, self.message.text()))
            
            
            
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            
            self.button7.setStyleSheet("border-radius: 10px;")
            keyboard.on_press_key("Enter", lambda _: send(self, self.message.text()))
            
            self.new_signal.emit("fa")
            
                  
            central.setLayout(self.client)




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

    
