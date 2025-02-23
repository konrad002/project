import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import select
HOST = "0.0.0.0"
PORT = 12345
messagesSent = []

def connect():
            print("are we even here?")
            print("are we here?")
            global s
            s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(2)
            
            
            while True:
                  global conn
                  conn, addr = s.accept()
                  
                  print("connected to", addr)
                  
                  
                  
            


class window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.client_socket = None
        
       
        
        self.resize(1000, 1000)
        self.setWindowTitle("Please wait for connection")
        
        self.label17 = QLabel("Please await for client to connect")
        self.label17.move(200,200)
        self.label17.setFont(QFont('Arial', 20))
      
        self.image = QLabel(self)
        pixelmap = QPixmap("pic.webp")
        self.label19 = QLabel(self)
        self.image.setPixmap(pixelmap)
        
        
        self.close()
        self.client_socket = newWindow()
        self.client_socket.show()
      
        layout = QVBoxLayout()
        layout.addWidget(self.label17)
        layout.addWidget(self.image)
        self.setLayout(layout)
        
        
      

        

class newWindow(QMainWindow):
      def __init__(self):
            super().__init__()
            

            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            navbar = self.menuBar()
            
            username = navbar.addMenu("Username")
            exit = QAction("Exit", self)
            exit.triggered.connect(self.close)
            self.message = QLineEdit(self)
            self.message.setGeometry(100, 500, 500, 100)
            self.button7 = QPushButton("Send",self)
            self.button7.setGeometry(50, 50, 50, 50)
            
            

            def send(message):
                  messagesSent.append(message)
                  conn.sendall(bytes(message, encoding='utf8'))
                  print(messagesSent)
            def receive():
                  while True:
                        ready, _, _ = select.select([s], [], [], 0.5)
                        if(ready):
                              data = conn.recv(1024)
                              
                              if(not data):
                                    print("disconnected")
                                    break
                              print(data)
                              messagesSent.append(data)
                              print(messagesSent)
            

            thread2 = threading.Thread(target=receive, daemon = True)
            thread2.start()

            rf = self.button7.clicked.connect(lambda: send(self.message.text()))
            print(rf, "line 83")
            self.show()
            

thread = threading.Thread(target=connect, daemon = True)
thread.start()

app = QApplication([])



window = window()
window.show()
 
app.exec()





