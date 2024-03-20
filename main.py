import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton, QFileDialog, \
    QDesktopWidget
from PyQt5.QtCore import Qt, QThread
import pandas as pd
import json
import os
from functools import partial
from PySide2.QtCore import Signal

import CVE_2019_13139 as CVE1
import CVE_2019_5736 as CVE2
import socketexploitfix as CVE3
pyQTfileName = "test_ui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(pyQTfileName)

##radioButtons = dict()


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        ##super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.resize(300,1000)
        self.resize(QDesktopWidget().availableGeometry(self).size() * 1.0)
        self.radioButtons = self.show_all_radio_buttons()
        self.page_1_label.setText('SURE-FIX\nSEcure Ubuntu Bionic\nREmedying Docker Vulnerabilities through Targeted FIXes')
        self.menu_button.clicked.connect(lambda: self.toggle_menu(250, True))
        self.Btn_1.clicked.connect(lambda: self.navigate_to_view_all('Display All Vulnerabilities'))
        self.Btn_3.clicked.connect(lambda: self.navigate_to_fix('Check and Fix'))
        self.Btn_4.clicked.connect(lambda: self.navigate_to_add_new('Add New Vulnerability'))
        self.Btn_fix.clicked.connect(lambda: self.fix_vulnerability())
        self.Btn_check.clicked.connect(lambda: self.check_vulnerability())

    def radio_button_action(self):
        text = self.sender().text()
        print('state changed '+text)
        if self.radioButtons[text][1]:
            self.Btn_fix.setEnabled(True)
        else:
            self.Btn_fix.setEnabled(False)


    ## support from https://github.com/Wanderson-Magalhaes/Toggle_Burguer_Menu_Python_PySide2/blob/master/ui_functions.py
    def toggle_menu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def navigate_to_view_all(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_2)
        self.page_2_label.setText(msg)

        # Import data
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_row = cve.shape[0]
        cve_col = cve.shape[1]

        # Set table
        self.Table_Cve.setColumnCount(cve_col)
        self.Table_Cve.setRowCount(cve_row)
        self.Table_Cve.setHorizontalHeaderLabels(cve.columns.values)
        self.Table_Cve.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # font = self.Table_Cve.horizontalHeader().font()
        # font.setBold(True)
        # self.Table_Cve.horizontalHeader().setFont(font)
        self.Table_Cve.horizontalHeader().setStyleSheet("color: rgb(0, 0, 0)")
        self.Table_Cve.verticalHeader().setStyleSheet("color: rgb(0, 0, 0)")

        # Add data into the table
        for i in range(len(cve)):
            # self.Table_Cve.setColumnWidth(i, 150)
            for j in range(len(cve.columns)):
                item = QTableWidgetItem(str(cve.iloc[i, j]))
                item.setTextAlignment(Qt.AlignCenter)
                # self.Table_Cve.setColumnWidth(j, 150)
                self.Table_Cve.setItem(i, j, item)




    def navigate_to_fix(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_4)
        self.page_4_label.setText(msg)
        self.Btn_fix.setEnabled(False)

    def navigate_to_add_new(self, msg):
        self.Page_widgets.setCurrentWidget(self.page_5)
        self.page_5_label.setText(msg)

        # Button action
        self.btn_browser.clicked.connect(self.file_add)
        self.btn_cve_add.clicked.connect(self.cve_add)
        self.btn_cve_modify.clicked.connect(self.cve_modify)

    def file_add(self):
        # choose a file
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'python files (*.py)')
        # split file path -> only file name
        fnamelist = fname[0].split('/')
        # set button text as file name
        self.btn_browser.setText(fnamelist[len(fnamelist)-1])


    def cve_add(self):
        # Get attributes fo new cve
        NewName = self.cve_name.toPlainText()
        NewDesc = self.cve_description.toPlainText()
        NewCVSS = float(self.cve_cvss.toPlainText())
        NewLink = self.cve_link.toPlainText()
        NewScript = self.btn_browser.text()

        # Store as dict
        NewDataDict = dict(CVE=NewName,
                    Description=NewDesc,
                    CVSS=NewCVSS,
                    Link=NewLink,
                    Script=NewScript)

        # update json file
        with open('test_data.json', 'r') as f:
            OldData = json.load(f)
        if len(OldData) > 1:
            OldData.append(NewDataDict)
        else:
            OldData = list(OldData)
        with open('test_data.json', 'w') as f_new:
            json.dump(OldData, f_new)
        self.outstate.setStyleSheet('color: rgb(255,255,255)')
        self.outstate.setPlainText('Success!')
    
    def cve_modify(self):
        # Get attributes fo new cve
        NewName = self.cve_name.toPlainText()
        NewDesc = self.cve_description.toPlainText()
        NewCVSS = self.cve_cvss.toPlainText()
        NewLink = self.cve_link.toPlainText()
        NewScript = self.btn_browser.text()

        # Open the json file to read cve information
        with open('test_data.json', 'r') as f:
            OldData = json.load(f)

        # Check whether the cve modified exists in the json file
        CveNameList = []
        for i in OldData:
            CveNameList.append(i['CVE'])
        if NewName in CveNameList:
            index = CveNameList.index(NewName)
            if len(NewDesc) > 0:
                OldData[index]['Description'] = NewDesc
            if len(NewCVSS) > 0:
                NewCVSS = float(NewCVSS)
                OldData[index]['CVSS'] = NewCVSS
            if len(NewLink) > 0:
                OldData[index]['Link'] = NewLink
            if len(NewScript) > 0 and NewScript != 'Browser':
                OldData[index]['Script'] = NewScript
            else:
                OldData[index]['Script'] = 'Not available'

            # update json file
            with open('test_data.json', 'w') as f_new:
                json.dump(OldData, f_new)
            self.outstate.setStyleSheet('color: rgb(255,255,255)')
            self.outstate.setPlainText('Success!')
        else:
            self.outstate.setStyleSheet('color: rgb(255,255,255)')
            self.outstate.setPlainText(f"{NewName} does not exist!\n Please try again!")

    def fix_vulnerability(self):
        # Import data
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_row = cve.shape[0]
        cve_col = cve.shape[1]
        msgbox = QMessageBox()
        msgbox1 = QMessageBox()
        msgbox1.setWindowTitle('Log Box')
        msg = ''
        for i, (k, v) in enumerate(self.radioButtons.items()):
            button = v[0]
            if button.isChecked():
                msg = button.text()
                print('%%%%'+msg)
                break
        msgbox.setText("Do you want to proceed with fixing this vulnerability?");
        msgbox.setStandardButtons(msgbox.Ok | msgbox.Cancel);
        msgbox.setWindowTitle('Message')
        ##msgbox.setDefaultButton(msgbox.Ok);
        ret = msgbox.exec_()

        if ret == int(msgbox.Ok):
            print('user clicked ok to fix ' + msg)
            if CVE1.get_name() == msg:
                result, log = CVE1.fix()
                if result:
                    msgbox1.setText(log+'\n'+"Successful Fix!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                else:
                    msgbox1.setText(log+'\n'+'Failed!!')
            elif CVE2.get_name() == msg:
                result, log = CVE2.fix()
                if result:
                    msgbox1.setText(log + '\n' + "Successful Fix!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                else:
                    msgbox1.setText(log + '\n' + 'Failed!!')
            elif CVE3.get_name() == msg:
                result, log = CVE2.fix()
                if result:
                    msgbox1.setText(log + '\n' + "Successful Fix!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                else:
                    msgbox1.setText(log + '\n' + 'Failed!!')
            else:
                msgbox1.setText('No fix available')
            msgbox1.exec_()

        else:
            print('user clicked cancel')

    def check_vulnerability(self):
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        msgbox = QMessageBox()
        msgbox1 = QMessageBox()
        msgbox1.setWindowTitle('Log Box')
        msg = ''
        description = ''
        for i, (k, v) in enumerate(self.radioButtons.items()):
            button = v[0]
            if button.isChecked():
                msg = button.text()
                description = cve.loc[cve['CVE'] == msg, 'Description'].iloc[0]
                print('%%%%'+msg)
                break
        msgbox.setText(description)
        msgbox.setInformativeText("Do you want to proceed with checking for this vulnerability?")
        msgbox.setStandardButtons(msgbox.Ok | msgbox.Cancel)
        msgbox.setWindowTitle('Description')
        ##msgbox.setDefaultButton(msgbox.Ok);
        ret = msgbox.exec_()
        if ret == int(msgbox.Ok):
            print('checking......')
            if CVE1.get_name() == msg:
                result, log = CVE1.check()
                if result:
                    msgbox1.setText('Checking...\n'+log+'\n'+"Vulnerability found!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                    self.radioButtons[msg][1] = True
                    self.Btn_fix.setEnabled(True)

                else:
                    self.Btn_fix.setEnabled(False)
                    self.radioButtons[msg][1] = False
                    msgbox1.setText('Checking...\n'+log+'\n'+'Vulnerability not found')
            elif CVE2.get_name() == msg:
                result, log = CVE2.check()
                if result:
                    msgbox1.setText('Checking...\n'+log + '\n' + "Vulnerability found!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                    self.radioButtons[msg][1] = True
                    self.Btn_fix.setEnabled(True)
                else:
                    self.Btn_fix.setEnabled(False)
                    self.radioButtons[msg][1] = False
                    msgbox1.setText('Checking...\n'+log + '\n' + 'Vulnerability not found!!')
            elif CVE3.get_name() == msg:
                result, log = CVE3.check()
                if result:
                    msgbox1.setText('Checking...\n'+log + '\n' + "Vulnerability found!!")
                    msgbox1.setStandardButtons(msgbox1.Ok)
                    self.radioButtons[msg][1] = True
                    self.Btn_fix.setEnabled(True)
                else:
                    self.Btn_fix.setEnabled(False)
                    self.radioButtons[msg][1] = False
                    msgbox1.setText('Checking...\n'+log + '\n' + 'Vulnerability not found!!')

            else:
                self.Btn_fix.setEnabled(False)
                msgbox1.setText('No checking available')
            msgbox1.exec_()
            print(self.radioButtons)
        else:
            print('Checking Cancelled!!')

    def show_all_radio_buttons(self):
        with open('test_data.json', 'r') as f:
            data = json.load(f)

        # Transfer into df and get shape
        cve = pd.DataFrame(data)
        cve_names = cve.loc[:, 'CVE'].tolist()
        print(cve_names)
        radio_buttons = dict()
        for i, name in enumerate(cve_names):
            ay = i*50+50
            button = QRadioButton(name, self.page_4)
            #button.setFixedWidth(190)
            #button.setFixedHeight(60)
            button.setGeometry(QtCore.QRect(0, ay, 300, 50))
            button.setStyleSheet('color: rgb(255,255,255); font-size: 18px')
            button.show()
            button.toggled.connect(self.radio_button_action)
            radio_buttons[name] = [button, False]
        return radio_buttons


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
