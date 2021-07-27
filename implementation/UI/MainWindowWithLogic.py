from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from implementation.UI.MainWindow import Ui_MainWindow
from datetime import datetime

from implementation.file_management.FileManagementLogic import FileManagementLogic
from implementation.file_management.DirectoryDescriptionCreator import DirectoryDescriptionCreator
from implementation.file_management.FileTypeConverter import FileTypeConverter
from implementation.file_management.ExtensionDictionary import ExtensionDictionary
from implementation.file_management.FileDescription import FileDescription

import math
import time


class MainWindow(QtWidgets.QMainWindow):
    COLOR_SUCCESS = 'green'
    COLOR_ERROR = 'red'
    RESULT_DIRECTORY = 'schedule2html_result'
    TIME_FORMAT = '%Y-%m-%d %H.%M.%S.%f'

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.sourceDirectoryButton.clicked.connect(self.getExcelSourceDirectory)
        self.ui.savingDirectoryButton.clicked.connect(self.getHTMLSavingDirectory)
        self.ui.JSONDirectoryPathChoiceButton.clicked.connect(self.getJSONDirectory)

        self.ui.JSONDirectoryPathActionButton.clicked.connect(self.createJSONDescriptionAction)

        self.ui.convertExcelToHTMLActionButton.clicked.connect(self.convertExcelToHTMLAction)
        self.createHtmlFilesThread = CreateHtmlFilesThread(self)

        self.createHtmlFilesThread.bridgeLog.connect(self.log)
        self.createHtmlFilesThread.bridgeSetWindowEnabledConfig.connect(self.setWindowEnabledConfig)
        self.createHtmlFilesThread.bridgeSetReportValue.connect(self.ui.report.setText)
        self.createHtmlFilesThread.bridgeProcessBarValue.connect(self.setProcessBarValue)

    def log(self, logString):
        self.ui.report.append(logString)

    def getErrorString(self, error: Exception):
        return '<h3><font color="{}">Произошла ошибка: </font></h3> <b>{}</b> <br>'.format(self.COLOR_ERROR, error)

    def getSuccessString(self):
        return '<h3><font color="{}">Операция успешно выполнена</font></h3>'.format(self.COLOR_SUCCESS)

    def getExcelSourceDirectory(self):
        self.getDirectory(self.ui.sourceExcelDirectoryPath)

    def getHTMLSavingDirectory(self):
        self.getDirectory(self.ui.savingHTMLDirectoryPath)

    def getJSONDirectory(self):
        self.getDirectory(self.ui.JSONDirectoryPath)

    def getDirectory(self, textInput: QtWidgets.QLineEdit) -> str:
        directory = QFileDialog.getExistingDirectory(self)
        textInput.setText(directory)
        return directory

    def convertExcelToHTMLAction(self):
        self.createHtmlFilesThread.start()

    def setWindowEnabledConfig(self, isEnabled):
        self.ui.tabWidget.setEnabled(isEnabled)

    def setProcessBarValue(self, value):
        value = math.floor(value)
        processBarMaximum = self.ui.progressBar.maximum()
        if value > processBarMaximum:
            value = processBarMaximum
        self.ui.progressBar.setValue(value)

    def createResultDirectoryName(self, userSavingDirectoryPath: str, needNewDirectory=False):
        result = userSavingDirectoryPath
        if needNewDirectory:
            result = result + '/' + self.RESULT_DIRECTORY + '_' + datetime.now().strftime(self.TIME_FORMAT)
        return result

    def createJSONDescriptionAction(self):
        try:
            directoryPath = self.ui.JSONDirectoryPath.text()
            self.checkDirectoryPath(directoryPath, 'Дирректории с html файлами')

            DirectoryDescriptionCreator().createJSONDescription(directoryPath, ExtensionDictionary.HTML_EXT)

            self.log(self.getSuccessString())
        except Exception as error:
            self.log(self.getErrorString(error))

    def checkDirectoryPath(self, directoryPath, pathTitle):
        if not FileManagementLogic().checkExistsPath(directoryPath):
            raise Exception('{0} ({1}) не найдена'.format(pathTitle, directoryPath))


class CreateHtmlFilesThread(QThread):
    COUNT_OPERATIONS_WITH_FILES = 4
    FIX_BUG_TIMEOUT = 2

    bridgeLog = pyqtSignal(str)
    bridgeSetWindowEnabledConfig = pyqtSignal(bool)
    bridgeSetReportValue = pyqtSignal(str)
    bridgeProcessBarValue = pyqtSignal(int)

    def __init__(self, obj: MainWindow, parent=None):
        super(CreateHtmlFilesThread, self).__init__(parent)
        self.obj = obj

    def run(self):
        processBarCurrentValue = 0
        try:
            self.setExecutingActionWindowSettings()
            self.bridgeProcessBarValue.emit(processBarCurrentValue)

            self.bridgeLog.emit('Проверка корректности введенных данных...')

            sourceDirectoryPath = self.obj.ui.sourceExcelDirectoryPath.text()
            savingDirectoryPathTmp = self.obj.ui.savingHTMLDirectoryPath.text()

            self.validateDirectoryPaths(sourceDirectoryPath, savingDirectoryPathTmp)

            needNewDirectory = self.obj.ui.createNewDirectoryCheckBox.isChecked()
            savingDirectoryPath = self.obj.createResultDirectoryName(savingDirectoryPathTmp, needNewDirectory)

            processBarCurrentValue += 5
            self.bridgeProcessBarValue.emit(processBarCurrentValue)

            files = self.getFiles(sourceDirectoryPath)

            processBarCurrentValue += 5
            self.bridgeProcessBarValue.emit(processBarCurrentValue)

            if len(files) != 0:
                processBarPercent = 75
                self.createHtmlFiles(files, sourceDirectoryPath, savingDirectoryPath, processBarPercent, processBarCurrentValue)
                processBarCurrentValue += processBarPercent
                self.bridgeProcessBarValue.emit(processBarCurrentValue)

                DirectoryDescriptionCreator().createJSONDescription(savingDirectoryPath, ExtensionDictionary.HTML_EXT)
                processBarCurrentValue += 15
                self.bridgeProcessBarValue.emit(processBarCurrentValue)

                messagePattern = '<h3><font color="{}">Операция успешно выполнена</font></h3>'
                self.bridgeLog.emit(messagePattern.format(self.obj.COLOR_SUCCESS))
        except Exception as error:
            messagePattern = '<h3><font color="{}">Произошла ошибка: </font></h3> <b>{}</b> <br>'
            self.bridgeLog.emit(messagePattern.format(self.obj.COLOR_ERROR, error))

        time.sleep(self.FIX_BUG_TIMEOUT)
        self.setActionCompletionWindowSettings()

    def setExecutingActionWindowSettings(self):
        self.bridgeSetWindowEnabledConfig.emit(False)
        self.bridgeSetReportValue.emit('')

    def setActionCompletionWindowSettings(self):
        self.bridgeProcessBarValue.emit(100)
        self.bridgeSetWindowEnabledConfig.emit(True)

    def validateDirectoryPaths(self, sourceDirectoryPath, savingDirectoryPath):
        self.obj.checkDirectoryPath(sourceDirectoryPath, 'Дирректории с исходными файлами')
        self.obj.checkDirectoryPath(savingDirectoryPath, 'Дирректории для сохранения')

    def getFiles(self, sourceDirectoryPath):
        self.bridgeLog.emit('Выполняется поиск Excel файлов...')
        files = FileManagementLogic().getAllFiles(sourceDirectoryPath, ExtensionDictionary.getExcelExtensions())
        self.bridgeLog.emit('Найдено: <b>{}</b> файлов'.format(len(files)))
        return files

    def getProcessBarStep(self, filesCount, percent: int):
        return percent / filesCount if filesCount > 0 else 0

    def createHtmlFiles(self, files, baseFilePath, baseSavingPath, processBarPercent, processBarCurrentValue) -> [[FileDescription]]:
        self.bridgeLog.emit('Создание HTML файлов...')
        processBarStep = self.getProcessBarStep(len(files), processBarPercent)

        newHtmlFiles = []
        for file in files:
            fileRelativePath = FileManagementLogic().getRelativePath(baseFilePath, file.getPath())
            newFilePath = FileManagementLogic().mergePath(baseSavingPath, fileRelativePath)
            htmlFilesList = FileTypeConverter().convertExcelToHtmlFiles(file, newFilePath)
            newHtmlFiles.append(htmlFilesList)
            for htmlFile in htmlFilesList:
                self.bridgeLog.emit('HTML файл {} создан'.format(htmlFile.getFullPath()))

            processBarCurrentValue += processBarStep
            self.bridgeProcessBarValue.emit(processBarCurrentValue)
        return newHtmlFiles
