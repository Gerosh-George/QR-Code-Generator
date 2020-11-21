from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrcode as qr

import sys

# class that instanstiates an image and converts qrcode image into qpixmap object
class ImageGenerator(qr.image.base.BaseImage):
    
    def __init__(self,border,width,box_size):
        
        self.border=border
        
        self.width=width
        
        self.box_size=box_size
        
        size= (width + border *2) * box_size
        
        self._image= QImage(size, size, QImage.Format_RGB16)
        
        self._image.fill(Qt.white)
    
    def getPixmap(self):
             
        return QPixmap.fromImage(self._image)   
    
    def drawrect(self, row,col):
        
        painter= QPainter(self._image)
        
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.darkMagenta)

# the main class that sets the properties of the GUI application
class GUIWindow(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)   
        
        self.setWindowTitle("QR CODE")
        
        self.setGeometry(100, 100, 350, 350)
        
        self.label = QLabel(self)
        
        self.label.setAlignment(Qt.AlignCenter)
        
        self.edit = QLineEdit(self)
        
        self.edit.returnPressed.connect(self.textHandler)        
        
        self.edit.setFont(QFont('Times',9))
        
        self.edit.setAlignment(Qt.AlignCenter)
        
        self.button= QPushButton("Copy the QR Code to Clipboard") 
        
        self.button.clicked.connect(self.copy)
        
        widget= QWidget()
        
        layout= QVBoxLayout(widget)
        
        layout.addWidget(self.label)
        
        layout.addWidget(self.edit)
        
        layout.addWidget(self.button)       
        
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
        
        self.image=None
        
    # function that takes in the text entered in the edit label and generates qr code
    def textHandler(self):
        
        text =self.edit.text()        
        qr_image=qr.make(text, image_factory = ImageGenerator).getPixmap()
        
        self.button.setText("Copy the QR Code to Clipboard")
        
        self.image=QPixmap.toImage(qr_image)
        self.label.setPixmap(qr_image)
    
    # function to copy the qr code image to the clipboard when user clicks the button
    def copy(self):
        if(self.edit.text() and self.image):             
            QApplication.clipboard().setImage(self.image)
            self.button.setText("Copied! 😄 ")
            
            
        


app = QApplication(sys.argv)

window= GUIWindow()

window.show()

sys.exit(app.exec_())
        
        