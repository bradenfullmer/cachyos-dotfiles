from urllib.request import urlopen, urlretrieve
from Core.UpdateInformation import UpdateInformation
from aqt.qt import *
from Global.Constants import *
import json
import os
import zipfile
import threading
import shutil

# The updater is currently not used, but may be useful for file management later (e.g. exchanging of the dictionary)

class CancelledException(Exception):
    def __init__(self):
        return

class AddonFolderMissing(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        return

class BootstrapperMissing(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        return

class Updater(QObject):

    _doneUpdateChecking = pyqtSignal()
    updateCheckTimeout = 8

    def __init__(self):
        super(QObject, self).__init__()
        self._updateInfoUrl = u"https://cutt.ly/2eg3oU6"
        self._updateInfo = UpdateInformation() #update information from the server is stored here
        self._updateInfo.addonVersion = u"1000.1000" #makes sure that no update is installed for the default value, I guess the addon never reaches version 1000 ;)

        self._progress = None

        self._addonsFolder = u""
        self._dlDestination = u""
        self._errorMessageUpdate = u""
        self._errorMessageUpdateCheck = u"Update check failed" #As long as nothing was checked, an error is assumed
        self._updateAvailable = False
        self._workerThread = None
        self._doneUpdateChecking.connect(self.onDoneUpdateChecking)

    def parallelUpdateCheck(self, installedMajor, installedMinor):
        self._workerThread = threading.Thread(target=self._checkForUpdates, args=(installedMajor, installedMinor))
        self._workerThread.start()

    def updateAvailable(self):
        if len(self._errorMessageUpdateCheck) != 0:
            raise Exception(self._errorMessageUpdateCheck)
        return self._updateAvailable

    def onDoneUpdateChecking(self):
        self._workerThread = None

    def setAddonsFolder(self, addonsFolder):
        self._addonsFolder = addonsFolder
        lastChar = addonsFolder[-1:]
        if lastChar != u"/" and lastChar != u"\\":
            self._addonsFolder += u"/"
        self._dlDestination = self._addonsFolder + u"LatestVersion.zip"

    def _checkForUpdates(self, installedMajor, installedMinor):
        try:
            with urlopen(self._updateInfoUrl, timeout=Updater.updateCheckTimeout) as response:
                downloadedData = response.read()
                self._updateInfo.fromDictionary(json.loads(downloadedData))

            serverMajorMinor = self._updateInfo.getMajorMinor()

            if self._updateInfo.testOnly:
                self._updateAvailable = False
            else:
                if serverMajorMinor[0] > installedMajor:
                    self._updateAvailable = True
                else:
                    self._updateAvailable = serverMajorMinor[1] > installedMinor

            self._errorMessageUpdateCheck = u""

        except Exception as e:
            self._errorMessageUpdateCheck = str(e)
        self._doneUpdateChecking.emit()
