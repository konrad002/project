
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from src_server.window import Window


app = QApplication([])
window = Window()
if(os.path.exists("temp/temp-server.json")):
     pass
else:
     window.show()

app.exec()

