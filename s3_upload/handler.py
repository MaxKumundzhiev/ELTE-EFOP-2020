# ------------------------------------------
#
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------
import os
import boto3
import logging
import argparse
import pandas as pd
import requests as re
from six import StringIO

from settings import APP

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DataUploader:
    """
    Description:
        Data Uploader Job assumed to download specifed data from TFL web application
        and upload to the dedicated S3 Bucket

    Arguments:
        --id   - TFL Application ID
        --key  - TFL Application KEY
        --year - Year of accidents to be downloaded

    Output:
        [Uploaded .csv file to the dedicated S3 Bucket]

    Example:
        [--id tfl_app_id --key tfl_app_key --year 2020]
    """

    def __init__(self, id, key, year):
        self.year = year
        self.target = 'tfl-accidents-{}.csv'.format(year)
        self.params = dict(app_id=id, app_key=key)

    def get_data(self):
        response = re.get(url='https://api.tfl.gov.uk/AccidentStats/{}'.format(self.year), params=self.params)
        return pd.DataFrame(response)

    def upload_s3(self, dataframe):
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer)
        client = boto3.client('s3')

        response = client.put_object(
            Body=csv_buffer.getvalue(),
            Bucket=APP['source'],
            Key=self.target
        )
        return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=APP['name'],
                                     description=APP['description'],
                                     epilog=APP['epilog'])

    parser.add_argument('--id', help="TFL Application Id", type=str, required=True)
    parser.add_argument('--key', help="TFL Application Key", type=str, required=True)
    parser.add_argument('--year', help='Accident Year', type=int, required=True)

    args = vars(parser.parse_args())

    data = DataUploader(**args).get_data()
    logging.info('Successfully Downloaded Accidents for {}'.format(args['year']))

    DataUploader(**args).upload_s3(data)
    logging.info('Successfully Uploaded Accidents for {} to S3 {}'.format(args['year'], APP['source']))