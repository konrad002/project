import socket
from PyQt5.QtWidgets import *
import select
import threading
from PyQt5.QtCore import pyqtSignal

messagesSent = []

layout = QVBoxLayout()
class window(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        
        
        self.mainlabel = QLabel("Client login ")
        self.label2 = QLabel("Enter IP and port number to connect")
        self.textbox1 = QLineEdit(self)
        self.textbox1.setPlaceholderText("Type IP address")
        self.textbox2 = QLineEdit(self)
        self.textbox2.setPlaceholderText("Type Port number")
        self.button = QPushButton('Connect')
        self.button2 = QPushButton('Go back')
        def on_click():
            alert = QMessageBox()
            global s
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.textbox1.text(), int(self.textbox2.text())))
                
            print("connected to server")
                
            
            self.client = newWindow()
            self.client.show()
                
        
                
                
                    

            
                    
            
        
        layout.addWidget(self.label2)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button)
        self.button.clicked.connect(on_click)
        self.setLayout(layout)
        



     
class newWindow(QMainWindow):
      new_signal = pyqtSignal(str)
      def __init__(self):
            
            super().__init__()
            
            
            def update_label(message):
                    text = str(messagesSent[-1])
                    label = QLabel(message)
                    layout.addWidget(label)
                    print(message)
                    label.setGeometry(500, 600, 500, 300)
                    label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px;")
                    
                    
                    
                

            self.resize(1000,1000)
            self.setWindowTitle("Client app")
            navbar = self.menuBar()
            self.label19 = QLabel("Client messenger ")
            username = navbar.addMenu("Username")
            exit = QAction("Exit", self)
            def send(message):
                messagesSent.append(message)
                s.sendall(bytes(message, encoding='utf8'))
                print(messagesSent)
                self.new_signal.emit(message)
      
                
            self.new_signal.connect(update_label)
            def receive():
                 while True:
                    ready, _, _ = select.select([s], [], [], 0.5)
                    if(ready):
                        data = s.recv(1024)
                        if(not data):
                            print("disconnected")
                            break
                        
                        message = data.decode("utf-8")
                        messagesSent.append(message)
                        print(messagesSent)
                        self.new_signal.emit(message)
                        
            

            thread = threading.Thread(target=receive, daemon = True)
            thread.start()
            
            
                    
             
           
            self.message = QLineEdit(self)
            self.message.setGeometry(100, 500, 500, 100)
            self.button7 = QPushButton("Send",self)
            self.button7.setGeometry(50, 50, 50, 50)
            r = self.button7.clicked.connect(lambda: send(self.message.text()))
            
            
            self.show()
            



app = QApplication([])
window = window()
window.show()
app.exec()