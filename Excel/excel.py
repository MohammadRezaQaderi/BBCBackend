from Excel.ms_excel import LoadExcelSourceFile
global master_file
global master_sheet


master_file = LoadExcelSourceFile(r'D:\WebSites\BBC\FileAG\Brain.xlsx')
master_sheet = master_file.sheets['نسخه هدایت تحصیلی انتخاب رشته']