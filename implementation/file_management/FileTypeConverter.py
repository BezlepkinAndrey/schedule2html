from implementation.file_management.FileDescription import FileDescription
from implementation.file_management.FileManagementLogic import FileManagementLogic
from implementation.file_management.ExtensionDictionary import ExtensionDictionary
import implementation.tools.Xlsx2HtmlConverter as Xlsx2Html
from xls2xlsx import XLS2XLSX
import openpyxl
import io
import codecs


class FileTypeConverter:

    def __init__(self):
        self.fileManagementLogic = FileManagementLogic()

    def convertExcelToHtmlFiles(self, file: FileDescription, savingPath: str) -> [FileDescription]:
        htmlFiles = []

        workbook = self.getExcelWorkBock(file)
        inputFileThread = io.BytesIO()
        workbook.save(inputFileThread)

        for sheetName in workbook.sheetnames:
            newHtmlFile = FileDescription(fileName=sheetName, ext=ExtensionDictionary.HTML_EXT, path=savingPath)

            self.fileManagementLogic.checkPossibilityCreatingFile(newHtmlFile)
            outputFileThread = Xlsx2Html.convert(inputFileThread, sheetName)

            inputFileThread.seek(0)
            outputFileThread.seek(0)

            resultHtml = outputFileThread.read()
            outputFileThread.close()

            self.writeHTMLFile(resultHtml, newHtmlFile)

            htmlFiles.append(newHtmlFile)

        inputFileThread.close()
        return htmlFiles

    def getExcelWorkBock(self, file: FileDescription) -> openpyxl.workbook.Workbook:
        if file.ext == ExtensionDictionary.XLS_EXT:
            return XLS2XLSX(file.getFullPath()).to_xlsx()
        else:
            return openpyxl.load_workbook(file.getFullPath(), data_only=True)

    def writeHTMLFile(self, html: str, file: FileDescription):
            self.fileManagementLogic.makeFileDirectory(file)
            fileThread = codecs.open(file.getFullPath(), "w", "utf-8")
            fileThread.write(html)
            fileThread.close()

