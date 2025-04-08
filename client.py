from PyQt5.QtWidgets import *
import os
from src_client.window import Window
       

app = QApplication([])
window = Window()
if(os.path.exists("temp/temp-client.json")):
     pass
else:
     window.show()
app.exec()