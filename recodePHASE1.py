#Lauren Magee
#Program 3

#Recode Part 1
#Took the CSV and made it into a Panda XLSX

import pandas as pd

data = pd.read_csv('training_data.csv', dtype=object)

writer = pd.ExcelWriter('D:\Documents\CS461/output.xlsx')
data.to_excel(writer)
writer.save()
