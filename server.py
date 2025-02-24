import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import pyqtSignal
import keyboard

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
        def on_click():
            alert = QMessageBox()
            global s, username_input
            
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
            
            
            
               
            
                
        
                
                
                    

            
                    
            
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.textbox3)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.textbox1)
        self.layout.addWidget(self.textbox2)
        self.layout.addWidget(self.button)
        
       
        self.button.clicked.connect(on_click)
        
        self.setLayout(self.layout)
        



     
class newWindow(QMainWindow):
      new_signal = pyqtSignal(str)
      def __init__(self):
            
            super().__init__()
            
            
            def update_label(message):
                    
                    label = QLabel(message)
                    
                    print(message)
                    
                    for user, msg in messagesSent:
                        if(user == "User 1"):
                            
                            message_layout = QHBoxLayout()
                            newLabel = QLabel("Anonymous")
                            label.setWordWrap(True)
                            newLabel.setStyleSheet("padding-right 10px;")
                            label.setStyleSheet("background-color: lightgray; padding: 5px; border-radius: 5px; height: 40px;")
                            message_layout.addStretch()
                            self.client.addLayout(message_layout)
                        elif(user == "User 2"):
                             message_layout = QHBoxLayout()
                             
                             newLabel = QLabel(username_input)
                             newLabel.setStyleSheet("padding: 5px;")
                             label.setStyleSheet("background-color: lightgreen; padding: 5px; border-radius: 5px; height: 50px;")
                             self.client.addLayout(message_layout)
                        
                    self.client.addWidget(label)
                    self.client.addWidget(newLabel)
                    
                    
                    
                

            self.resize(1000,1000)
            self.setWindowTitle("Client app")
            navbar = self.menuBar()
            self.label19 = QLabel("Client messenger ")
            
            navbar.addMenu(username_input)
            exit = QAction("Exit", self)
            def send(message):
                if(message == ""):
                    return
                messagesSent.append(("User 2", message))
                
                s.sendall(bytes(message, encoding='utf8'))
                

                print(message, 2421841)
                print(s.getsockname())
                print("does this get run here?")
                print(messagesSent)
                self.message.setText("")
                self.new_signal.emit(message)
      
                
            self.new_signal.connect(update_label)
            def receive():
                 while True:
                    ready, _, _ = select.select([s], [], [], 0.5)
                    print(ready)
                    if(ready):
                        data = s.recv(1024)

                        if(not data):
                            print("disconnected")
                            break
                        
                        message = data.decode("utf-8")
                        messagesSent.append(("User 1", message))
                        print(messagesSent)
                        self.new_signal.emit(message)
                        
            

            thread = threading.Thread(target=receive, daemon = True)
            thread.start()
            
            
                    
             
            central = QWidget()
            self.setCentralWidget(central)
            self.client = QVBoxLayout()
            self.message = QLineEdit(self)
            self.message.setGeometry(100, 500, 500, 100)
            self.button7 = QPushButton("Send",self)
            self.message.setPlaceholderText("Type in a message to send")
            self.button7.setGeometry(50, 50, 50, 50)
            r = self.button7.clicked.connect(lambda: send(self.message.text()))
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            self.button7.setStyleSheet("border-radius: 10px;")
            keyboard.on_press_key("Enter", lambda _: send(self.message.text()))
            central.setLayout(self.client)

            
            
            



app = QApplication([])
window = window()
window.show()
app.exec()