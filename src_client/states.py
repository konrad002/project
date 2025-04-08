import socket
class States:
      def __init__(self):
            hostname = str(socket.gethostname())
            self.HOST = socket.gethostbyname(hostname)
            self.s = None
            self.state0 = False
            self.loading = False
            self.client = None
            self.client_username = ""
            self.isReady = None
            self.username = ""
            self.messagesSent = []
            self.pastConnections = {}
            self.username_input = ""
            self.count = 0
            

states = States()