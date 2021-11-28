import pandas as pd
import requests
import os

dataType = "StatePopulation"
with open('census_key.txt') as key:
    api_key = "&key=" + key.read().strip()

years = pd.read_csv("Years.csv")
#for year in years.index:
#    print(years.iloc[year]['Year'], years.iloc[year]['Root_Query'], years.iloc[year]['State_Query'])
excel_dict = dict()
for year in years.index:
    print("Retrieving ", years.iloc[year]['Year'], dataType, " Data...")
    response = requests.get(years.iloc[year]['State_Query'] + api_key)
    data = response.json()
    df = pd.DataFrame(data)
    excel_dict[years.iloc[year]['Year']]=dict()
    for (i, entry) in enumerate(data):
        if i == 0: continue
        excel_dict[years.iloc[year]['Year']][entry[1]]=int(entry[0])
    path = f"{years.iloc[year]['Year']}\\{dataType}\\"
    if not os.path.isdir(path): os.makedirs(path)
    fileName = f"{years.iloc[year]['Year']}{dataType}.csv"
    df.to_csv(os.path.join(path, fileName), index=False, header=False)
    #df.to_csv(f"{years.iloc[year]['Year']}StatePopulation.csv", index=False, header=False)

excel_DataFrame = pd.DataFrame(excel_dict)
writer = pd.ExcelWriter("StatePopulation.xlsx", engine='xlsxwriter')
excel_DataFrame.to_excel(writer, sheet_name='Sheet1')
workbook = writer.book
worksheet = writer.sheets['Sheet1']
chart = workbook.add_chart({'type': 'column'})
#spreadsheets are row, col zero based index
chart.add_series({
    'name': ['Sheet1', 0, 1],
    'categories': '=Sheet1!A$2:$A$53',
    'values': '=Sheet1!$B2:$B$53'})
chart.add_series({
    'name': '=Sheet1!$C$1',
    'categories': '=Sheet1!A$2:$A$53',
    'values': '=Sheet1!$C2:$C$53'})
chart.add_series({
    'name': '=Sheet1!$D$1',
    'categories': '=Sheet1!A$2:$A$53',
    'values': '=Sheet1!$D2:$D$53'})
worksheet.insert_chart('F2', chart)
writer.save()
#print(excel_DataFrame)

