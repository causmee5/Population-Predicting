'''COMP2006HWFinalProject - Kemmler & Ausmees
This project uses population data sets obtained from the US Census Bureau. The data sets are state population data
and county population data. The objective of this project is to predict population increases and decreases for each
state and county for the year 2010. Projections will be made using 1990 and 2000 data and will then be compared to
the actual census data of 2010.'''

import pandas as pd
import numpy as np
import logging as logit
from os import listdir
import argparse, csv
from collections import defaultdict

class ReadConfig():

    def __init__(self):
        self.configuration = dict()
        self.state_map_list = list()

    def read_file_locs(self, file):
        self.configuration = pd.read_csv(file, index_col=0, squeeze=True).to_dict()
        #print(self.configuration)

    def read_state_map(self, file):
        self.state_map_list = pd.read_csv(file, header=None, squeeze=True).tolist()
        #print(self.state_map_list)

    def get_path(self, year):
        return self.configuration.get(int(year))


class ReadCountyData():

    def __init__(self, config):
        #print all files
        self.config_instance = config
        self.file_1990 = None
        self.file_2000 = None
        self.county_dict_1990 = defaultdict(lambda: "Not Present")
        self.county_dict_2000 = defaultdict(lambda: "Not Present")
        self.county_dict_2010 = defaultdict(lambda: "Not Present")
        self.columns = None
        self.county_pop_by_year = dict()
        self.county_pop_projections = dict()
        self.year_to_dict_map = {1990: self.county_dict_1990, 2000: self.county_dict_2000, 2010: self.county_dict_2010}

    def get_file(self, dir, state):
        files = listdir(dir)
        for entry in files:
            if state.lower() in entry.lower():
                return dir + entry

    def clean_county_name(self, data_dict):
        new_dict = {}
        for key, val in data_dict.items():
            new_name = key.split(', ', 1)
            #print(new_name[0])
            #new_dict.update({new_name: val})
            new_dict[new_name[0]] = val

        '''sub_string = ', '
        for (idx, ser) in data.iterrows():
            clean_string = list(ser[self.columns[1]].split(', ', 1))
            data.at[idx, self.columns[1]] = clean_string
            #data[self.columns[1]].astype('str').value_counts()
            #print(data.loc[idx, self.columns[1]])
            #print(ser.values)
            #data.loc[idx, self.columns[1]] = data.loc[idx, self.columns[1]].split(', ', 1)
            #data.loc[idx, self.columns[1]] = data.loc[idx, self.columns[1]].replace(', Florida', '')
            #new_value = list(ser[self.columns[1]].split(', ', 1))
            #new_value = list(ser[self.columns[1]].replace(', Florida', ''))
            #data.update({ser[self.columns[1]]: new_value})
        return data'''
        return new_dict

    def build_county_dict(self, path):
        '''with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:'''
        csv_data = pd.read_csv(path)
        self.columns = csv_data.columns
        #csv_data = self.clean_county_name(csv_data)
        df = pd.DataFrame(csv_data)
        df.set_index(self.columns[1], inplace=True)
        return df.to_dict()[self.columns[0]]

    def create_county_pop_by_year(self):
        print("Finding data differences between years...")
        dict_diffs = self.county_dict_1990.keys() - self.county_dict_2000
        print(dict_diffs)
        dict_diffs2 = self.county_dict_2000.keys() - self.county_dict_2010
        print(dict_diffs2)
        for key, val in self.county_dict_2010.items():
            self.county_pop_by_year[key] = {}
            self.county_pop_by_year[key][2010] = val
            try:
                self.county_pop_by_year[key][2000] = self.county_dict_2000[key]
            except:
                print("County Not Found in 2000 Data: ", key)
            try:
                self.county_pop_by_year[key][1990] = self.county_dict_1990[key]
            except:
                print("County Not Found in 1990 Data: ", key)
        print(self.county_pop_by_year)

    def update_year_dict_map(self):
        self.year_to_dict_map[1990] = self.county_dict_1990
        self.year_to_dict_map[2000] = self.county_dict_2000
        self.year_to_dict_map[2010] = self.county_dict_2010

    def get_projection(self, y1, y2):
        self.update_year_dict_map()
        arr = np.array([y1, y2])
        year1_dict = self.year_to_dict_map[y1]
        year2_dict = self.year_to_dict_map[y2]
        projection_dict = dict()

        for key, value in year1_dict.items():
            projection_dict[key] = {}
            increase = value - year2_dict[key]
            percent_change = increase/year2_dict[key] * 100
            projection_dict[key]['2010P'] = percent_change
            increase2010 = self.county_dict_2010[key] - self.county_dict_2000[key]
            percent_change2010 = increase2010/self.county_dict_2000[key] * 100
            projection_dict[key]['2010A'] = percent_change2010
        return projection_dict


    def project_county_population(self, state):
        file_1990 = self.get_file(self.config_instance.get_path(1990), state)
        #print(file_1990)
        self.county_dict_1990 = self.build_county_dict(file_1990)
        #print(self.county_dict_1990)
        file_2000 = self.get_file(self.config_instance.get_path(2000), state)
        #print(file_2000)
        self.county_dict_2000 = self.build_county_dict(file_2000)
        #print(self.county_dict_2000)
        file_2010 = self.get_file(self.config_instance.get_path(2010), state)
        #print(file_2010)
        self.county_dict_2010 = self.build_county_dict(file_2010)
        self.county_dict_2010 = self.clean_county_name(self.county_dict_2010)
        #print(self.county_dict_2010)
        self.create_county_pop_by_year()

        print(self.get_projection(2000, 1990))




if __name__ == '__main__':
    # Main Function
    # Setup logging
    logger = logit.getLogger()
    logger.setLevel(logit.DEBUG)
    # Add file logging and set level
    fh = logit.FileHandler('COMP3006HW-FP.log', 'w')
    fh.setLevel(logit.DEBUG)
    logger.addHandler(fh)
    # Add console/shell logging and set level
    sh = logit.StreamHandler()
    sh.setLevel(logit.INFO)
    logger.addHandler(sh)

    # Read in configuration data - file locations
    config = ReadConfig()
    config.read_file_locs("./COMP3006HWFinalProjectConfigurationFile.config")
    #for key in config.configuration:
    #    ReadCountyData(config, key)
    #Read state map
    state_map = ReadConfig()
    state_map.read_state_map("./state_map.config")

    # Parse arguments
    parser = argparse.ArgumentParser(description='Project county population for a state.')
    #parser.add_argument('print', metavar='<print>', type=str, help='Iterate over the elements of the AutoMPGData \
    #                    collection (as it is sorted) and print each one.')
    parser.add_argument('-s', '--state', type=str, help='Provide state. Will project population for all counties', choices=state_map.state_map_list)
    #parser.add_argument('-c', '--county', type=str, help='Provide a county.')
    #parser.add_argument('-y', '--year', help='Project population change for year', choices=['2010', '2020'])
    args = parser.parse_args()

    cd = ReadCountyData(config)
    cd.project_county_population(args.state)


