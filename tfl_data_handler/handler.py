# ------------------------------------------
#
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------
import json
import pandas as pd
import requests as re
import argparse
from tfl_data_handler.settings import type_dict

class DataUpload:
    def __init__(self, tfl_credentials, year):
        self.params = tfl_credentials
        self.year = year

    def DataTransform(self):
        response =  re.get(url='https://api.tfl.gov.uk/AccidentStats/{}'.format(self.year), params=self.params)
        json = pd.read_json(response)
        return json

    # def transform_json(self):
    #     df.to_csv (r'Path where the new CSV file will be stored\New File Name.csv', index=None)
    #     return


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('--id', help="TFL Application Id", type=int, required=True)
    # parser.add_argument('--key', help="TFL Application Key", type=int, required=True)
    # parser.add_argument('--year', help='Accident Year', type=int, required=True)
    #
    # args = parser.parse_args()
    #
    # DataUpload(**args).run()

    json_data_2018 = DataUpload(type_dict, 2018).upload_json()
    print(json_data_2018)
