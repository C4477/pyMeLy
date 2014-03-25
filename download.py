#!/usr/bin/env python
import xml.etree.ElementTree as et
import urllib as u
import zipfile
import os.path, sys, os, shutil, time
from PyQt4 import QtCore, QtGui, uic

t1 = time.clock()

key = '3E7E5A05D3C6236A'

def firstdl():
    #Initial downloading of metadata, to find show ID.
    initial_xml = 'xml/shows.xml'
    #Create folder for initial metadata if it does not already exist
    if not os.path.isdir('xml/initial'):
        print 'Creating folder xml/initial/'
        os.mkdir('xml/initial')
    #Parse XML file containing show list
    print 'Parsing initial XML file.'
    tree = et.parse(initial_xml)
    root = tree.getroot()
    #Read XML file, download metadata matching each TV show listed
    for child in root:
        for grandchild in child:
            if os.path.isfile('xml/initial/%s.xml' % grandchild.text):
                print 'Initial metadata for %s already downloaded.' % grandchild.text
            else:
                print 'Downloading initial metadata for %s.' % grandchild.text
                u.urlretrieve("http://thetvdb.com/api/GetSeries.php?seriesname=%s" % grandchild.text, 'xml/initial/%s.xml' % grandchild.text)
    print 'Finished downloading initial metadata.'

def seconddl():
    #Additional downloading of metadata, to find all info about show
    #Create folder for additional metadata if it does not already exist
    if not os.path.isdir('xml/additional'):
        print 'Creating folder xml/additional/'
        os.mkdir('xml/additional')
    #Downloads additional metadata
    for showinitial in os.listdir('xml/initial'):
        showid = get_id('xml/initial/%s' % showinitial)
        if os.path.isfile('xml/additional/%s.zip' % showid):
            print 'Additional metadata for show with ID %s already downloaded.' % showid
        else:
            print 'Downloading show with ID %s' % showid
            u.urlretrieve('http://thetvdb.com/api/%s/series/%s/all/en.zip' % (key, showid), 'xml/additional/%s.zip' % showid)
            #Extract downloaded zip to its own directory
            extract('xml/additional/%s.zip' % showid, 'xml/additional/%s' % showid)
    #Delete zip files
    print 'Cleaning up temporary files'
    cleanup('.zip', 'xml/additional')
    print 'Finished downloading additional metadata.'

def get_id(target):
    #Finds ID of show from XML file
    tree = et.parse(target)
    root = tree.getroot()
    showid = root[0][0].text
    return showid

def extract(target, destination):
    #Extracts contents to its own directory
    with zipfile.ZipFile(target, 'r') as z:
        z.extractall(destination)
        z.close()

def cleanup(filetype, directory):
    #Cleans a directory of files of a given file type
    for _file in os.listdir(directory):
        if _file.lower().endswith(filetype):
            os.remove('%s/%s' % (directory, _file))

firstdl()
seconddl()

t2 = time.clock()
total = t2 - t1
print 'Time taken: ' + str(total)
