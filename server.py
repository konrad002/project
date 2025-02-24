import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import select

hostname = str(socket.gethostname())
HOST = socket.gethostbyname(hostname)

PORT = 12345
messagesSent = []
conn = None
def connect():
            print("are we even here?")
            print("are we here?")
            
            global s, conn
            
            s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(2)
            
            
            while True:
                  
                  conn, addr = s.accept()
                  print(conn)
                  print("connected to", addr)
                  
                  
                  
            


class window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.client_socket = None
        
       
        
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
        
        
        self.close()
        self.client_socket = newWindow()
        self.client_socket.show()
      
        layout = QVBoxLayout()
        layout.addWidget(self.label17)
        self.label17.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ip)
        self.ip.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ip2)
        self.ip2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image)
        self.image.setScaledContents(True)
        
        self.setLayout(layout)
        
        
      

        

class newWindow(QMainWindow):
      new_signal = pyqtSignal(str)
      def __init__(self):
            super().__init__()
            username_input = None
            if(username_input == None):
                  alert = QMessageBox()
                  alert.setText("Enter username")
                  alert.exec_()
            self.resize(1000,1000)
            self.setWindowTitle("Server app")
            navbar = self.menuBar()
            
            username = navbar.addMenu("Username")
            exit = QAction("Exit", self)
            exit.triggered.connect(self.close)
            
           
            
            def update_label(message):
                    
                    label = QLabel(message)
                    
                    print(message)
                    for user, msg in messagesSent:
                        if(user == "User 2"):
                             message_layout = QHBoxLayout()
                             
                             newLabel = QLabel("Temporary name")
                             newLabel.setStyleSheet("padding: 5px;")
                             label.setStyleSheet("background-color: lightgray; font-size: 14px; padding: 5px; border-radius: 5px; height: 50px;")
                             self.client.addLayout(message_layout)
                        elif(user == "User 1"):
                            message_layout = QHBoxLayout()
                            newLabel = QLabel("Anonymous")
                            
                            newLabel.setStyleSheet("padding-right 10px;")
                            label.setStyleSheet("background-color: lightgreen; font-size: 14px; padding: 5px; border-radius: 5px; height: 40px;")
                    self.client.addWidget(label)
                    self.client.addWidget(newLabel)

            def send(message):
                  messagesSent.append(("User 1", message))
                  conn.sendall(bytes(message, encoding='utf8'))
                  print(messagesSent)
                  self.new_signal.emit(message)
            
            self.new_signal.connect(update_label)
            def receive():
                  global conn

                  while True:
                        if conn == None:
                              continue

                        ready, _, _ = select.select([conn], [], [], 0.5)
                        print(ready, "line 119")
                        
                        if(ready):
                              data = conn.recv(1024)
                              print("this has been run")
                              if(not data):
                                    print("disconnected")
                                    break
                              print(data)
                              message = data.decode("utf-8")
                              messagesSent.append(("User 2", message))
                              print(messagesSent)
                              self.new_signal.emit(message)
                              print("what about this?")
            

            thread2 = threading.Thread(target=receive, daemon = True)
            thread2.start()

            central = QWidget()
            self.setCentralWidget(central)
            self.client = QVBoxLayout()
            self.message = QLineEdit(self)
            self.message.setGeometry(100, 500, 500, 100)
            self.button7 = QPushButton("Send",self)
            self.button7.setGeometry(50, 50, 50, 50)
            self.button7.clicked.connect(lambda: send(self.message.text()))
            self.client.addWidget(self.message)
            self.client.addWidget(self.button7)
            self.button7.setStyleSheet("border-radius: 10px;")
            central.setLayout(self.client)
            

thread = threading.Thread(target=connect, daemon = True)
thread.start()

app = QApplication([])



window = window()
window.show()
 
app.exec()





