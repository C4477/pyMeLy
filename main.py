#!/usr/bin/env python
import setup, sys
from PyQt4 import QtCore, QtGui, uic

def playVideo(url):            
    media = Phonon.MediaObject()
    media.setCurrentSource(Phonon.MediaSource(url))
    media.play()    

def pauseVideo():
    

app = QtGui.QApplication(sys.argv)
window = uic.loadUi('video.ui')
QObject.connect(self.ppButton, QtCore.SIGNAL("clicked()"), playPause)
window.show()
sys.exit(app.exec_())
