import pandas as pd
import requests
import os

dataType = "CountyPopulation"

with open('census_key.txt') as key:
    api_key = "&key=" + key.read().strip()

years = pd.read_csv("Years.csv")#File Containing the years Census data available with year specific queries

#for year in years.index:
#    print(years.iloc[year]['Year'], years.iloc[year]['Root_Query'], years.iloc[year]['Root_Query'])

dtype_dict = {'state': str} #This data type dictionary is needed to account for state numbers that have leading zeros.

for year in years.index:
    #x = 0
    # Use dtype so state numbers are read as strings to keep the leading zeros.
    stateDataFile = f"{years.iloc[year]['Year']}\\StatePopulation\\{years.iloc[year]['Year']}StatePopulation.csv"
    if not os.path.isfile(stateDataFile):
        print("File does not exist: ", stateDataFile)
        break
    else:
        stateData = pd.read_csv(stateDataFile, dtype=dtype_dict)
    for entry in stateData.index:
        print(f"Getting and saving {dataType} data for: ", years.iloc[year]['Year'], " ", stateData.iloc[entry][1], " ",
              str(stateData.iloc[entry]['state']))
        query = years.iloc[year]['County_Query'] + stateData.iloc[entry]['state'] + api_key
        #print(query)
        response = requests.get(query)
        #print(response.text)
        data = response.json()
        df = pd.DataFrame(data)
        path = f"{years.iloc[year]['Year']}\\{dataType}\\"
        if not os.path.isdir(path): os.makedirs(path)
        fileName = f"{years.iloc[year]['Year']}{stateData.iloc[entry][1]}{dataType}.csv"
        df.to_csv(os.path.join(path, fileName), index=False, header=False)
        #x += 1
        #if x >= 2: break

