import keyboard
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
import json


def ui_window(self):
          


          self.mainlabel = QLabel("Client login ")
          self.username = QLabel("Enter your username")
          self.textbox3 = QLineEdit(self)
          self.label2 = QLabel("Enter your password")
          self.password = QLineEdit(self)
          self.password.setPlaceholderText("Type in password")
          print(self.states.username, "this is username")
          self.button = QPushButton('Connect')
          
          self.layout = QVBoxLayout()
          self.layout.addWidget(self.mainlabel)
          self.layout.addWidget(self.username)
          self.layout.addWidget(self.textbox3)
          self.layout.addWidget(self.label2)
          self.layout.addWidget(self.password)
          
          self.layout.addWidget(self.button)
          
          
          #keyboard.on_press_key("Enter", lambda _: self.on_click()) //use later
          self.button.clicked.connect(self.on_click)

          self.setLayout(self.layout)    

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

          
          
def ui_chatApp(self):
          
          self.resize(1000,1000)
          self.setWindowTitle("Client app")
          self.states.navbar = self.menuBar()
          self.states.navbar.addMenu(self.states.username_input)
          self.states.navbar.setStyleSheet("color: blue;")

          
          
          

          self.main_layout = QHBoxLayout(self) #main layout
          

          self.chat_area = QWidget()
          self.chat_area_layout = QVBoxLayout()
          self.chat_area.setLayout(self.chat_area_layout)
          
          
          
          self.scroller = QScrollArea()
          self.scroller.setWidgetResizable(True)
          
          
          #self.client = QWidget() #part of main layout, client window
          self.message = QLineEdit(self)
          self.message.setGeometry(100, 500, 500, 100)
          self.button7 = QPushButton("Send",self)
          self.message.setPlaceholderText("Type in a message to send")
          self.button7.setGeometry(50, 50, 50, 50)
          self.button7.clicked.connect(lambda: send(self, self.message.text()))
          self.button = QPushButton()
          self.button.setIcon(QIcon("img/chat.jpg"))
          self.button.setIconSize(QSize(50, 50))
          self.button.setFixedSize(60, 60)
          self.button.setStyleSheet("border: none; background-color: transparent;")  
            
          
          

          self.button7.setStyleSheet("border-radius: 10px;")
          keyboard.on_press_key("Enter", lambda _: send(self, self.message.text()))
          self.banner = QLabel("placeholder")
          self.banner.hide()
          
          
          self.new_signal.emit("far")
          self.main_layout.addWidget(self.button)
          self.main_layout.addWidget(self.message)
          self.main_layout.addWidget(self.button7)
          self.main_layout.addWidget(self.banner)
          self.main_layout.addWidget(self.chat_area)