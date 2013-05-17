#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from widgets import MainWidget
from parser import Parser
import time
from lib.utils.mail import sendInformationMail
from lib.utils.firewall import dropIncomingPacketsFromHost
from lib.fuzzy.variable import Variable
from lib.fuzzy.fuzzyengine import FuzzyEngine
from lib.fuzzy.fuzzyrule import FuzzyRule
from lib.fuzzy.membershipfunction import MembershipFunction


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.hostHistory = {}
        self.blockedHosts = []
        self.informedHosts = []

        self.scheduler = QtCore.QTimer()
        self.scheduler.start(1000)
        QtCore.QObject.connect(self.scheduler, QtCore.SIGNAL("timeout()"), self.printHosts)
    
        self.request = Variable("Request")
        self.request.membershipFunctions["Low"] = MembershipFunction("Low", 0, 0, 25, 75)
        self.request.membershipFunctions["Middle"] = MembershipFunction("Middle", 35, 60, 80, 150)
        self.request.membershipFunctions["High"] = MembershipFunction("Hot", 75, 150, 250, 1000)

        self.degree = Variable("Degree")
        self.degree.membershipFunctions["Low"] = MembershipFunction("Low", 0, 0, 5, 25)
        self.degree.membershipFunctions["Middle"] = MembershipFunction("Middle", 25, 45, 55, 75)
        self.degree.membershipFunctions["High"] = MembershipFunction("High", 75, 95, 100, 100)

        self.fe = FuzzyEngine()
        self.fe.variables["Request"] = self.request
        self.fe.variables["Degree"] = self.degree

        self.fe.calculatedVariable = self.degree

        self.fe.fuzzyRules.append(FuzzyRule("IF (Request IS Low) THEN Degree IS Low"))
        self.fe.fuzzyRules.append(FuzzyRule("IF (Request IS Middle) THEN Degree IS Middle"))
        self.fe.fuzzyRules.append(FuzzyRule("IF (Request IS High) THEN Degree IS High"))

        self.initUI()
    
    def printHosts(self):
        self.mw.textEdit.clear()
        self.mw.textEdit.append("Total number of requests by host:\n")
        
        for host, request in self.parser.hosts.items():
            if time.time() - request['lastUpdated'] > 10:
                del self.parser.hosts[host]
                continue
            passedTime = time.time() - request['startTime']#calculate how much time passed
            reqPersec = request['count'] / passedTime
            print "Req Per Sec: " + str(reqPersec)
            self.request.inputValue = reqPersec
            result = self.fe.defuzzify()

            if result > 0 and result <=25:
                if host in self.blockedHosts:
                    status = "Blocked "
                elif host in self.informedHosts:
                    status = "Informed"
                else:
                    status = "No action"

            elif result > 25 and result <=75:
                if host in self.blockedHosts:
                    status = "Blocked"
                elif host in self.informedHosts:
                    status = "Informed"
                elif not host in self.informedHosts:
                    sendInformationMail(host)
                    self.informedHosts.append(host)
                    status = "Informed"

            if result > 75 and result <=100:
                if not host in self.blockedHosts:
                    #uncomment this line to block host
                    #dropIncomingPacketsFromHost(host) 
                    self.blockedHosts.append(host)
                    pass
                else:
                    pass
                status = "Blocked"

            self.mw.textEdit.append("%s -----------> Number of total request: %s - %s per/sec - %s - %s\n" % (host, request['count'], reqPersec, result, status))

    def initUI(self):               
        self.mw = MainWidget()        
        self.setCentralWidget(self.mw)
        self.parser = Parser("/var/log/apache2/access.log")
        self.parser.start()

        self.statusBar().showMessage('Parser is executed.')

        exitAction = QtGui.QAction(QtGui.QIcon().fromTheme("exit"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Apache Dos Detector')    
        self.show()
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.scheduler.stop()
            event.accept()
        else:
            event.ignore()        
         
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 
