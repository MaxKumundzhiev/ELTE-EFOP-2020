# ------------------------------------------
#
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------
import os
import json
import argparse
import logging
import boto3
import pandas as pd
import requests as re
from botocore.exceptions import ClientError
from six import StringIO
#from tfl_data_handler.settings import LOGGER


class DataUpload:
    def __init__(self, id, key, year):
        self.year = year
        self.bucket_name = 'tfl-accidents-{}'.format(year)
        self.params = dict(
            app_id=id,
            app_key=key
        )

    def get_data(self):
        response = re.get(url='https://api.tfl.gov.uk/AccidentStats/{}'.format(self.year), params=self.params)
        return pd.DataFrame(response)

    def s3_create_bucket(self):
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        try:
            s3.create_bucket(Bucket=self.bucket_name,
                             CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
            if self.bucket_name in response:
                logging.info('There are already existing Bucket')
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def s3_upload(self, dataframe):
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer)
        client = boto3.client('s3')
        response = client.put_object(
            Body=csv_buffer.getvalue(),
            Bucket=self.bucket_name,
            Key='{}.csv'.format(self.bucket_name)
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', help="TFL Application Id", type=str, required=True)
    parser.add_argument('--key', help="TFL Application Key", type=str, required=True)
    parser.add_argument('--year', help='Accident Year', type=int, required=True)

    args = vars(parser.parse_args())

    data = DataUpload(**args).get_data()
    logging.info('Data downloaded successfully')

    # DataUpload(**args).s3_create_bucket()
    # logging.info('Bucket created successfully')

    DataUpload(**args).s3_upload(data)
    logging.info('Data uploaded successfully')
