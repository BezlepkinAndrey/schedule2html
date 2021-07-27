from implementation.file_management.FileDescription import FileDescription

import os
import re


class FileManagementLogic:

    def checkExistsPath(self, path: str) -> bool:
        return os.path.exists(path)

    def createFileDescription(self, path: str, fileNameWithExt: str) -> FileDescription:
        fileName, ext = os.path.splitext(fileNameWithExt)
        return FileDescription(fileName=fileName, ext=ext, path=path)

    def getRelativePath(self, basePath, fullPath) -> str:
        return fullPath.replace(basePath, '')

    def mergePath(self, first, second) -> str:
        splitData = self.splitPath(first)
        splitData.extend(self.splitPath(second))
        return '/'.join(splitData)

    def splitPath(self, path) -> [str]:
        return list((filter(bool, re.split(r'[/\\]', path))))

    def makeFileDirectory(self, fileDescription: FileDescription):
        os.makedirs(fileDescription.getPath(), exist_ok=True)

    def removeFile(self, fileDescription):
        os.remove(fileDescription.getFullPath())

    def getAllFiles(self, directory: str, exts: ()) -> [FileDescription]:
        foundFiles = []
        for root, dirs, files in os.walk(directory):
            foundFiles += [self.createFileDescription(root, fileNameWithExt)
                           for fileNameWithExt in files if fileNameWithExt.endswith(exts)]
        return foundFiles

    def checkPossibilityCreatingFile(self, file: FileDescription):
        if self.checkExistsPath(file.getFullPath()):
            raise Exception('Файл <b> {} </b> уже существует, операция невозможна!'.format(file.getFullPath()))