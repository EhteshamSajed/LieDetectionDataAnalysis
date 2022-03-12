from openpyxl import Workbook, load_workbook

filePath = "ExcelExport/"

# def createOrOpen(fileFullPath):
    

def exportAllAvg():
    fileName = "AllAverages.xlsx"
    wb = Workbook()
    ws = wb.active
    ws['A1'].value = "1234"
    wb.save(filePath+fileName)

exportAllAvg()