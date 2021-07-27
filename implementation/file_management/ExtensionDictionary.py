class ExtensionDictionary:
    XLS_EXT = '.xls'
    XLSX_EXT = '.xlsx'
    HTML_EXT = '.html'
    JSON_EXT = '.json'

    @staticmethod
    def getExcelExtensions():
        return ExtensionDictionary.XLSX_EXT, ExtensionDictionary.XLS_EXT