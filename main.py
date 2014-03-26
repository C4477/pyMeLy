#!/usr/bin/env python
import setup, sys
from PyQt4 import QtCore, QtGui, uic

app = QtGui.QApplication(sys.argv)
window = uic.loadUi('video.ui')
window.show()
sys.exit(app.exec_())
