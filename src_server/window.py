import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import select
import keyboard
import bcrypt
import json
from datetime import datetime
import os
import time
from src_server.states import *
from src_server.newWindow import newWindow


class Window(QWidget):
      def __init__(self):

            super().__init__()
      
            self.states = states
            self.reconnecting = False 
            
            
            
            self.thread = threading.Thread(target=self.connect, daemon = True)
            self.thread.start()
            self.active_windows = []
      
      
            
      
      

            if(os.path.exists("temp/temp-server.json")):
                  self.get_username()
                  self.reconnecting = True

                  
            
            if(not self.reconnecting):
                  self.ui_window()

      

      

      def ui_window(self):
          self.mainlabel = QLabel("Server login ")
          self.username = QLabel("Enter your username")
          self.textbox3 = QLineEdit(self)
          self.label2 = QLabel("Enter your password")
          self.password = QLineEdit(self)
          self.password.setPlaceholderText("Type in password")
          

          print(self.states.username, "this is username")
          self.button = QPushButton('Connect')
          self.button2 = QPushButton('Go back')
          self.layout = QVBoxLayout()
          self.layout.addWidget(self.mainlabel)
          self.layout.addWidget(self.username)
          self.layout.addWidget(self.textbox3)
          self.layout.addWidget(self.label2)
          self.layout.addWidget(self.password)
          self.hashed = bcrypt.hashpw(self.password.text().encode("utf-8"), bcrypt.gensalt())
          self.states.server_password = self.hashed.decode()
          print(self.states.server_password)
          self.layout.addWidget(self.button)
          #keyboard.on_press_key("Enter", lambda _: self.on_click()) //use later
          self.button.clicked.connect(self.on_click)
          print("jk")
          self.setLayout(self.layout)  
      
      def run_newWindow(self):
            self.close()
            self.states.client = newWindow(self)
            self.states.client.show()

      def on_click(self):
            
        
               
               #if(bcrypt.checkpw(self.states.something, self.states.server_password) == False): #TODO
               #   raise Exception("Incorrect password")
            try:
                  self.states.username = self.textbox3.text()
                  
                  

                  print(self.states.server_password, self.states.username, "these are the 2 values")
                  
                  if(self.states.username == ""):
                        print("it is empty")
                  if(self.states.server_password != "" and self.states.username != ""):
                        if("$" in self.states.username):
                              raise ValueError()
                        print(1)
                        if(self.states.conn != None):
                              print(2)
                              self.run_newWindow()
               
                        else:
                              print(3)
                              self.something()
            except ValueError:
                  self.alert_error("Username cannot contain $")
            except Exception:
                  self.alert_error("Something went wrong...")
            
            print(self.states.conn)
               
            print("connected to client!")

      def alert_error(self, error):
            alert = QMessageBox()
            alert.setText(error)
            alert.setWindowTitle("Error")
            alert.setIcon(QMessageBox.Icon.Warning)
            alert.setStandardButtons(QMessageBox.StandardButton.Ok)
            alert.exec_()    
      def get_username(self):
         
            
            print(self.thread.is_alive(), 3)
         
            
            
            label_username = QMessageBox()
            label_username.setIcon(QMessageBox.Information)
            label_username.setText("Want to relogin?")
            label_username.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            r = label_username.exec_()
            if(r == QMessageBox.Ok):
                   
                  with open('temp/temp-server.json', 'r') as output:
                        r = json.load(output)
                        print(r)
                        self.states.client_username = r[0]["client_user"]
                        self.states.username = r[0]["server_user"] 

                        self.states.client_password = r[0]["client_password"].decode()
                        self.states.server_password = r[0]["server_password"].decode()
                        
                        #if(bcrypt.checkpw(self.states.something, self.states.password) == False): #TODO
                        #      raise Exception("Incorrect password")
                              
                        f = r[1:len(r)]
                        for k in f:
                              
                              self.states.messagesSent.append((k["user"], k["username"], k["message"], k["time"]))
                        print(r)
                        
                        self.states.loading = True
                        
                        print("run?")
                        print(self.states.messagesSent)
                        output.close()
                        self.states.state0 = True
                  print("surely this gets printed out no?")
                   
                  self.something()

                             
            elif(r == QMessageBox.Cancel):
                  os.remove("temp/temp-server.json")
                 
                  self.ui_window()
            else:
                  exit()
         
            
              
         
         
            
      def something(self):
            
            
         
         
         
            while(self.states.isReady == False):
            

                  print(self.states.isReady, "fhiasge")        
            
                  label4 = QMessageBox()
                  label4.setText("Waiting to reconnect... ")
                  label4.setStyleSheet("")
                        
                  label4.setWindowTitle(self.username.text() + " " + "relogin?")
                  QTimer.singleShot(2000, label4.close)
                              
                  label4.exec_()
                  try:
                        print(11)
                        
                        recv = self.states.conn.recv(1024).decode()
                        print(22)
                        k = recv[0:2]
                        print(k)
                        print(33)
                        if(k == "$2b$" or k == "$2a$"):
                              self.states.client_password = recv
                        print(44)
                        print(self.states.client_password)
                        print(55)
                        f = self.states.conn.recv(1024).decode()
                        print(f, "client_useranme")
                        print(66)
                        self.states.client_username = f
                        print(77)
                        print(self.states.client_username, "this is the client username guys")
                  except:
                        pass
                  if(self.states.conn != None):
                        print("there is now a new connection")
                        self.states.isReady = True
                        
                        
                        return
                  if(self.thread.is_alive() == False):
                        print("running connect")
                        self.thread = threading.Thread(target=self.connect, daemon = True)
                        self.thread.start()
                  
                  print(self.thread.is_alive)
            
      
         
            
            
      def reuse(self):
            
            if(self.states.check_state != None):
                  print("xz")
                  self.states.navbar.clear()
                  self.states.navbar.addMenu(self.states.username)
                  
                  self.states.loading = None
            else:  
                  print("zx2", self.states.check_state)
                  self.states.check_state = 1
                  self.states.loading = True
                  QTimer.singleShot(0, self.show_window)

      def connect(self):
           
            
            print("are we even here?")
            print("are we here?")
          
      
            
      
            try:
                  self.states.s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
                  self.states.s.bind((self.states.HOST, 12345))
                  self.states.s.listen(1)
                  self.states.conn, self.states.addr = self.states.s.accept()
            except Exception as e:
                  print("j")
                  print(e)
                  exit()     
                  
      
      
                  
      
            
      

            print("connected now")
            while(self.states.state0 == False and self.reconnecting == True):
                  pass
            print(self.states.state0, self.reconnecting)
            if(os.path.exists("temp/temp-server.json")):
                  
             
                  print("//??")
                  self.states.conn.sendall(b"ready")
                  print("s")
                  confirm = self.states.conn.recv(1024).decode()
                  print(confirm, "this is confirm")
                  if(confirm == "confirmed"):
                        z = True
                        while(z):
                              try: 
                                    self.states.pastConnections["client"] = self.states.client_username     
                                    self.states.pastConnections["server"] = self.states.username
                                    print(self.states.username, "just now sending username to client")
                                    
                                    

                                    z = False
                                    print("username and client username have both been defined")
                              except:
                                    print("still waiting")
                        self.states.isReady = True
                        
                        self.reuse()
                        
                        
                        
                  
                        
            else:
                  self.states.isReady = True
                  print("fsf")
                  j = self.states.conn.recv(1024).decode()
                  print(j, "this is meant to be the username line 314")
                  for k in j:
                        index = k.find("$")
                        if(k == "$"):
                              self.states.client_password = j[index:]
                              break
                        self.states.client_username += k
                  self.states.pastConnections["server"] = self.states.username
                  self.states.pastConnections["client"] = self.states.client_username
                  print(self.states.pastConnections)
                  print(self.states.client_username, "client username")
                  
                  self.reuse()
      

    
      def show_window(self):
            
            print("was this even run?")
            self.close()
            self.states.client_socket = newWindow(self)
            self.states.client_socket.show()
            self.active_windows.append(self)
            
            
            print("connected to", self.states.addr)
            print(self.states.pastConnections, "line 163")
            print(self.active_windows)

        
          
            