from typing import TypeVar
import os

FileT = TypeVar('FileT', bound='File')


class FileDescription:
    def __init__(self, path: str, fileName: str, ext: str):
        self.fileName = fileName
        self.ext = ext
        self.path = path

    def getFileName(self) -> str:
        return self.fileName

    def getExt(self) -> str:
        return self.ext

    def getPath(self) -> str:
        return self.path

    def setExt(self, ext: str):
        self.ext = ext

    def setBasePath(self, path: str):
        self.path = path

    def setFileName(self, fileName: str):
        self.fileName = fileName

    def getFullPath(self) -> str:
        return os.path.join(self.path, self.fileName + self.ext)
