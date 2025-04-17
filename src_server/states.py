import socket
class States:
      def __init__(self):
            hostname = str(socket.gethostname())
            self.HOST = socket.gethostbyname(hostname)
            self.s = None
            self.PORT = 12345
            self.messagesSent = []
            self.conn = None
            self.pastConnections = {}
            self.loading = False
            self.disconnected = False
            self.navbar = None
            self.state0 = False
            self.check_state = None
            self.client_username = ""
            self.username = ""
            
            self.client_password = ""
            self.server_password = ""
            self.isReady = False
            self.client_socket = None 
            
           
            

states = States()