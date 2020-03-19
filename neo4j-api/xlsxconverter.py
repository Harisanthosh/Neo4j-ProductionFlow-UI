import pandas as pd
from xlsx2csv import Xlsx2csv
# Create empty table
path=r'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/H164632.GLOBAL/'
#output_table.to_csv(path+'export_router_0001.csv',encoding='utf-8-sig',sep=',',index=False)
Xlsx2csv(path+'export_assy_0001.xlsx', outputencoding="utf-8").convert("assy.csv")
