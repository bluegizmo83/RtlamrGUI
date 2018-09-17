import sys
import os
import subprocess
import datetime
import time
import win32api
from PyQt4 import uic
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtCore import QTimer, QThread, pyqtSignal

Ui_MainWindow, QtBaseClass = uic.loadUiType("RtlamrGUI.ui")

# Global varibles #
process = None
process1 = None
MyThread1 = None
MyThread2 = None
ui = None

# Rtlamr GUI window class #
class MyApp(QMainWindow):
         
    def __init__(self):
        super(MyApp, self).__init__()
        global ui
        ui = Ui_MainWindow()
        ui.setupUi(self)
        
        def done1(dataReceived):
            self.dataReceived = dataReceived
            ui.dataReceived.append(self.dataReceived)
            
        def startstopnow():
            if ui.startButton.text() == 'START':
                startstop().start()
            elif ui.startButton.text() == 'STOP':
                startstop().stop()


        global MyThread1
        global MyThread2
        MyThread1 = rtlamr()
        MyThread1.MySignal1.connect(done1)
        MyThread2 = rtl_tcp()
                                                                   
        ui.startButton.clicked.connect(startstopnow)

    def __del__(self):
        MyThread1.terminate()
        MyThread2.terminate()

# GUI Start/Stop button control class #
class startstop():

    def start(self):
        print('start class running')
        radiobuttons = [ui.msgtype_all, ui.msgtype_scm, ui.msgtype_scmplus, ui.msgtype_idm, ui.msgtype_netidm, ui.msgtype_r900, ui.msgtype_r900bcd]
        radiobuttonslen = len(radiobuttons)
        for i in range(0, radiobuttonslen):
            if radiobuttons[i].isChecked():
                radiobuttonsplit = radiobuttons[i].objectName().split('_')
                selectedradiobutton = radiobuttonsplit[1]
        if ui.uniquecheck.checkState() == 0:
            uniquecheck = 'False'
        elif ui.uniquecheck.checkState() == 2:
            uniquecheck = 'True'
        MyThread2.setVaribles(ui.deviceindex.value())
        MyThread2.start()
        time.sleep(2)
        MyThread1.setVaribles(ui.filterID.toPlainText(), selectedradiobutton, uniquecheck)
        MyThread1.start()
        ui.startButton.setText('STOP')
            
    def stop(self):
        print('stop class running')
        MyThread1.quit()
        MyThread2.quit()
        process.terminate()
        process1.terminate()
        ui.startButton.setText('START')
        print('stopped')

# Rtlamr.exe process thread #
class rtlamr(QThread):
    MySignal1 = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def setVaribles(self, filterIDbox, selectedradiobutton, uniquecheck):
        self.filterIDbox = '-filterid=' + str(filterIDbox)
        self.selectedradiobutton = '-msgtype=' + str(selectedradiobutton)
        self.uniquecheck = '-unique=' + str(uniquecheck)
        print self.filterIDbox
        print self.selectedradiobutton
        print self.uniquecheck

    def run(self):
        try:
            global process
            CREATE_NO_WINDOW = 0x08000000
            
            if self.filterIDbox != '-filterid=':
                process = subprocess.Popen('rtlamr %s %s %s' % (self.filterIDbox, self.selectedradiobutton, self.uniquecheck), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        print('RTLAMR filtered Readline Buffer Empty, break.')
                        break
                    if output:
                        self.MySignal1.emit(output.strip())
                        print output.strip()
                        
            else:
                process = subprocess.Popen('rtlamr %s %s' % (self.selectedradiobutton, self.uniquecheck), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        print('RTLAMR unfiltered Readline Buffer Empty, break.')
                        break
                    if output:
                        self.MySignal1.emit(output.strip())
                        print output.strip()

                        
        except:
            print('rtlamr failed to connect to rtl_tcp. Device Index may be incorrect.')
            startstop().stop()
            


# Rtl_tcp.exe process thread #
class rtl_tcp(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def setVaribles(self, deviceindex):
        self.deviceindex = str(deviceindex)

    def run(self):
        try:
            print('rtl_tcp STARTED, Device Index ' + self.deviceindex)
            global process1
            CREATE_NO_WINDOW = 0x08000000
            self.startcmd = 'rtl_tcp -d %s' % self.deviceindex
            process1 = subprocess.Popen(self.startcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
            while True:
                    output = process1.stdout.readline()
                    if output == '' and process.poll() is not None:
                        print('RTL_TCP Readline Buffer Empty, break.')
                        break
                    if output:
                        print ('FLAG')
        except:
            print('Error starting rtl_tcp.exe, Device Index may be wrong.')
            time.sleep(3)
            startstop().stop()
            win32api.MessageBox(0, 'Error starting rtl_tcp.exe, Device Index may be wrong.', 'rtl_tcp.exe error', 0x00001000)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MyApp()
        window.show()
        sys.exit(app.exec_())
    finally:
        
        try:
            process.terminate()
        except:
            pass
        
        try:
            process1.terminate()
        except:
            pass
