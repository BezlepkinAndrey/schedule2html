from implementation.file_management.FileDescription import FileDescription
from implementation.file_management.FileManagementLogic import FileManagementLogic
from implementation.file_management.ExtensionDictionary import ExtensionDictionary

import json
import os

DEFAULT_JSON_DESCRIPTION_FILE_NAME = 'description'


class DirectoryDescriptionCreator:

    def __init__(self, descriptionFileName=DEFAULT_JSON_DESCRIPTION_FILE_NAME):
        self.descriptionFileName = descriptionFileName
        self.fileManagementLogic = FileManagementLogic()

    def createJSONDescription(self, directoryPath: str, exts: ()):
        files = self.fileManagementLogic.getAllFiles(directoryPath, exts)
        dictDescription = self.createDictDescription(directoryPath, files)
        file = FileDescription(fileName=self.descriptionFileName, ext=ExtensionDictionary.JSON_EXT, path=directoryPath)

        with open(file.getFullPath(), 'w') as f:
            json.dump(dictDescription, f)

    def createDictDescription(self, directoryPath, files: [FileDescription]):
        jsonData = {'files': [], 'directories': {}}
        for file in files:
            tmpJson = jsonData
            fileRelativePath = self.fileManagementLogic.getRelativePath(directoryPath, file.getPath())
            for directory in self.fileManagementLogic.splitPath(fileRelativePath):
                if directory not in tmpJson['directories']:
                    tmpJson['directories'][directory] = {'files': [], 'directories': {}}
                tmpJson = tmpJson['directories'][directory]
            fullFileRelativePath = os.path.join(fileRelativePath, file.getFileName() + file.getExt());
            tmpJson['files'].append({'file_name': file.getFileName(), 'relativePath': fullFileRelativePath})
        return jsonData
