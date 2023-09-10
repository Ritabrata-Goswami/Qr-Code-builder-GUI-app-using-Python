import sys
import os
import shutil
from datetime import date

import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image
from pyzbar import pyzbar
import random
from cryptography.fernet import Fernet

from PyQt5 import *
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot


class create_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Python Qr Generator Desktop App'
        self.left = 450
        self.top = 150
        self.width = 700
        self.height = 600
        self.create_qr_app_UI()


    def create_qr_app_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.header_one = QLabel(self)
        self.header_one.setText("QR Generator App")
        self.header_one.move(15, 5)
        self.header_one.resize(250, 45)
        self.header_one.setStyleSheet("font-size: 20pt; font-weight:bold; font-family:Arial;")
        
        self.label_1 = QLabel(self)
        self.label_1.setText("Enter Item Name:")
        self.label_1.move(15, 75)
        self.label_1.resize(200, 45)
        self.textbox_1 = QLineEdit(self)
        self.textbox_1.move(150, 75)
        self.textbox_1.resize(300, 35)
        self.label_1.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        self.textbox_1.setStyleSheet("font-size: 11pt;")

        self.label_2 = QLabel(self)
        self.label_2.setText("Enter Item Id:")
        self.label_2.move(15, 120)
        self.textbox_2 = QLineEdit(self)
        self.textbox_2.move(150, 120)
        self.textbox_2.resize(300, 35)
        self.label_2.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        self.textbox_2.setStyleSheet("font-size: 11pt;")

        label_3 = QLabel(self)
        label_3.setText("Manufacture Location:")
        label_3.move(15, 160)
        label_3.resize(250, 45)
        self.manufacture_location = QComboBox(self)
        self.manufacture_location.addItem('-select-')
        self.manufacture_location.addItem('Kolkata Plant')
        self.manufacture_location.addItem('Delhi Plant')
        self.manufacture_location.addItem('Hydrabad Plant')
        self.manufacture_location.addItem('Chennai Plant')
        self.manufacture_location.addItem('Bengaluru Plant')
        self.manufacture_location.move(195, 165)
        self.manufacture_location.resize(150, 35)
        self.manufacture_location.setStyleSheet("font-size: 12pt;")
        label_3.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        self.manufacture_location.activated.connect(self.get_location)

        label_dest = QLabel(self)
        label_dest.setText("Destination Location:")
        label_dest.move(15, 205)
        label_dest.resize(250, 45)
        self.warehouse_location = QComboBox(self)
        self.warehouse_location.addItem('-select-')
        self.warehouse_location.addItem('Bhubaneswar Warehouse')
        self.warehouse_location.addItem('Delhi Warehouse')
        self.warehouse_location.addItem('Mumbai Warehouse')
        self.warehouse_location.addItem('Kolkata Warehouse')
        self.warehouse_location.addItem('Durgapur Warehouse')
        self.warehouse_location.addItem('Loknow Warehouse')
        self.warehouse_location.addItem('Patna Warehouse')
        self.warehouse_location.addItem('Ranchi Warehouse')
        self.warehouse_location.addItem('Guwahati Warehouse')
        self.warehouse_location.addItem('Siliguri Warehouse')
        self.warehouse_location.addItem('Agartala Warehouse')
        self.warehouse_location.move(195, 210)
        self.warehouse_location.resize(220, 35)
        self.warehouse_location.setStyleSheet("font-size: 12pt;")
        label_dest.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        self.warehouse_location.activated.connect(self.get_warehouse_location)

        label_4 = QLabel(self)
        label_4.setText("Transportation mode:")
        label_4.move(15, 250)
        label_4.resize(250, 45)
        self.radiobutton_1 = QRadioButton(self)
        # self.radiobutton.setChecked(True)
        self.radiobutton_1.country = "road"
        self.radiobutton_1.toggled.connect(self.onclicked_transport)
        self.radiobutton_1.move(195, 258)
        radiobutton_text_1 = QLabel(self)
        radiobutton_text_1.setText("By Road")
        radiobutton_text_1.move(210, 258)
        label_4.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        radiobutton_text_1.setStyleSheet("font-size: 12pt; font-family:Arial;")

        self.radiobutton_2 = QRadioButton(self)
        self.radiobutton_2.country = "air"
        self.radiobutton_2.toggled.connect(self.onclicked_transport)
        self.radiobutton_2.move(285, 258)
        radiobutton_text_2 = QLabel(self)
        radiobutton_text_2.setText("By Air")
        radiobutton_text_2.move(300, 258)
        radiobutton_text_2.setStyleSheet("font-size: 12pt; font-family:Arial;")

        self.radiobutton_3 = QRadioButton(self)
        self.radiobutton_3.country = "sea"
        self.radiobutton_3.toggled.connect(self.onclicked_transport)
        self.radiobutton_3.move(355, 258)
        radiobutton_text_3 = QLabel(self)
        radiobutton_text_3.setText("By Sea")
        radiobutton_text_3.move(370, 258)
        radiobutton_text_3.setStyleSheet("font-size: 12pt; font-family:Arial;")

        self.radiobutton_4 = QRadioButton(self)
        self.radiobutton_4.country = "rail"
        self.radiobutton_4.toggled.connect(self.onclicked_transport)
        self.radiobutton_4.move(435, 258)
        radiobutton_text_4 = QLabel(self)
        radiobutton_text_4.setText("By Rail")
        radiobutton_text_4.move(450, 258)
        radiobutton_text_4.setStyleSheet("font-size: 12pt; font-family:Arial;")

        label_date = QLabel(self)
        label_date.setText("Manufacture Date:")
        label_date.move(15, 320)
        label_date.resize(250, 45)
        label_date.setStyleSheet("font-size: 12pt; font-weight:bold; font-family:Arial;")
        
        label_date_info = QLabel(self)
        label_date_info.setText("Click on date field to get current date")
        label_date_info.move(160, 290)
        label_date_info.resize(500, 45)
        label_date_info.setStyleSheet("font-size: 11pt; font-family:Arial; color:red;")

        label_date_format = QLabel(self)
        label_date_format.setText("m/d/yyyy")
        label_date_format.move(270, 327)
        label_date_format.resize(500, 45)
        label_date_format.setStyleSheet("font-size: 11pt; font-family:Arial;")
        today = date.today()
        self.date_edit = QDateEdit(self)
        self.date_edit.move(160, 327)
        self.date_edit.setDate(today)
        self.date_edit.setStyleSheet("font-size: 12pt; font-family:Arial;")
        self.date_edit.editingFinished.connect(self.update_date)

        self.button = QPushButton('Generate Qr', self)
        self.button.move(150,410)
        self.button.setStyleSheet("background:#00802b; color:#ffffff; font-size:15px;")
        self.button.clicked.connect(self.generate_qr_img)

        #cpoyright
        label_cpoyright = QLabel(self)
        label_cpoyright.setText("Developed and Updated By Ritabrata Goswami.")
        label_cpoyright.move(15, 450)
        label_cpoyright.resize(500, 45)
        label_cpoyright.setStyleSheet("font-size: 8pt; font-family:Arial; font-style:italic;")

        self.textbox_get_location = QLineEdit(self)
        self.textbox_get_location.move(150, 500)
        self.textbox_get_location.resize(300, 35)
        self.textbox_get_location.hide()

        self.textbox_get_mode = QLineEdit(self)
        self.textbox_get_mode.move(150, 540)
        self.textbox_get_mode.resize(300, 35)
        self.textbox_get_mode.hide()

        self.textbox_get_warehouse = QLineEdit(self)
        self.textbox_get_warehouse.move(150, 580)
        self.textbox_get_warehouse.resize(300, 35)
        self.textbox_get_warehouse.hide()

        self.textbox_get_date = QLineEdit(self)
        self.textbox_get_date.move(150, 620)
        self.textbox_get_date.resize(300, 35)
        self.textbox_get_date.hide()

        self.show()

    def get_location(self):
        loc_val = self.manufacture_location.currentText()
        self.textbox_get_location.setText(str(loc_val))
        print(loc_val)
    
    def onclicked_transport(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            transport_val = radioButton.country
            self.textbox_get_mode.setText(str(transport_val))
            print(transport_val)
    
    def get_warehouse_location(self):
        loc_val = self.warehouse_location.currentText()
        self.textbox_get_warehouse.setText(str(loc_val))
        print(loc_val)

    def update_date(self): 
        date_val = self.date_edit.date()
        print(date_val)
        self.textbox_get_date.setText(str(date_val.toPyDate()))

    def generate_qr_img(self):
        text_box_val_1 = self.textbox_1.text()
        text_box_val_2 = self.textbox_2.text()
        text_box_val_3 = self.textbox_get_location.text()
        text_box_val_4 = self.textbox_get_mode.text()
        text_box_val_5 = self.textbox_get_warehouse.text()
        text_box_val_6 = self.textbox_get_date.text()

        popup = QMessageBox()

        if text_box_val_1=="" or text_box_val_2=="" or text_box_val_3=="" or text_box_val_4=="" or text_box_val_5=="" or text_box_val_3=="-select-" or text_box_val_5=="-select-" or text_box_val_6=="": 
            popup.setWindowTitle("Warning")
            popup.setIcon(QMessageBox.Warning)
            popup.setText("Field's Should Not Be Left Blank!")
            popup.setStyleSheet("font-size:13px;")
            popup.exec_()
        else:
            cont_string = text_box_val_1+"&"+text_box_val_2+"&"+text_box_val_3+"&"+text_box_val_4+"&"+text_box_val_5+"&"+text_box_val_6
            key = Fernet.generate_key()
            key_object = Fernet(key)
            encoded_text = key_object.encrypt(cont_string.encode())
            url = pyqrcode.create(encoded_text)
            url.png(r'C:\Users\abc123\Desktop\python\python desktop app\QR code generator\QR_gen_folder\Qr_'+text_box_val_2+'.png', scale = 12, module_color="#3333ff")
            print('Success!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = create_app()
    sys.exit(app.exec())