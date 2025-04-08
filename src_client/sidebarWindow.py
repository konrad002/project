from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class sidebarWindow(QWidget):
     def __init__(self):
          super().__init__()
          self.ui_sidebarWindow()
     def ui_sidebarWindow(self):
          layout = QVBoxLayout()
          layout.setAlignment(Qt.AlignTop)
          layout.setSpacing(15)
          #1
          self.button = QPushButton()
          self.button.setIcon(QIcon("img/chat.jpg"))
          self.button.setIconSize(QSize(50, 50))
          self.button.setFixedSize(60, 60)
          self.button.setStyleSheet("border: none; background-color: transparent;")
          
          layout.addWidget(self.button)
          self.setLayout(layout)
          self.setFixedWidth(50)
          #for k in range(4):
          #     button = QPushButton(f"Item {k + 1}")
          #     button.setFixedSize(60, 60)
          #     button.setStyleSheet("""
          #                         border-radius: 30px;
          #                         background-color: #5865F2;
          #                         color: white;
          #                         font-weight: bold;
          #                          """)
          #     layout.addWidget(button)
          #self.setStyleSheet("background-color: #121117;")
          #self.setLayout(layout)
          
          