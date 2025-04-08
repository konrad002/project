import keyboard
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from src_client.network import send

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


def run_app(self):
          self.close()
          self.client = ui_window(self)
          self.client.show()
          
def ui_chatApp(self):
          global navbar
          self.resize(1000,1000)
          self.setWindowTitle("Client app")
          navbar = self.menuBar()
          navbar.addMenu(self.states.username_input)
          navbar.setStyleSheet("color: blue;")

          
          
          

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
          self.button7.clicked.connect(lambda: send(self.message.text()))
          self.button = QPushButton()
          self.button.setIcon(QIcon("img/chat.jpg"))
          self.button.setIconSize(QSize(50, 50))
          self.button.setFixedSize(60, 60)
          self.button.setStyleSheet("border: none; background-color: transparent;")  
            
          
          

          self.button7.setStyleSheet("border-radius: 10px;")
          keyboard.on_press_key("Enter", lambda _: send(self.message.text()))
          self.banner = QLabel("placeholder")
          self.banner.hide()
          
          
          self.new_signal.emit("far")
          self.main_layout.addWidget(self.button)
          self.main_layout.addWidget(self.message)
          self.main_layout.addWidget(self.button7)
          self.main_layout.addWidget(self.banner)
          self.main_layout.addWidget(self.chat_area)