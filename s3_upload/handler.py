# ------------------------------------------
#
# Program created by Maksim Kumundzhiev
#
#
# email: kumundzhievmaxim@gmail.com
# github: https://github.com/KumundzhievMaxim
# -------------------------------------------
import boto3
import logging


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

    def download_from_tfl(self):
        import json
        response = re.get(url='https://api.tfl.gov.uk/AccidentStats/{}'.format(self.year), params=self.params).text
        json_data = json.loads(response)
        df = pd.DataFrame(json_data)
        return df

    def upload_to_s3(self, dataframe):
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer)
        client = boto3.client('s3')

        response = client.put_object(
            Body=csv_buffer.getvalue(),
            Bucket=APP['source'],
            Key=self.target
        )
        return response

    def save_data_local(self, data):
        data.to_csv(f'{APP["local_dir"]}/{self.year}.csv', index=False)
        return True

    def main(self):
        data = self.download_from_tfl()
        logging.info('Successfully Downloaded Accidents for {}'.format(args['year']))

        self.save_data_local(data)
        logging.info(f'Saved Accidents data for {args["year"]} under {APP["local_dir"]}')

        self.upload_to_s3(data)
        logging.info('Successfully Uploaded Accidents for {} to S3 {}'.format(args['year'], APP['source']))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog=APP['name'],
                                     description=APP['description'],
                                     epilog=APP['epilog'])

    parser.add_argument('--id', help="TFL Application Id", type=str, required=True)
    parser.add_argument('--key', help="TFL Application Key", type=str, required=True)
    parser.add_argument('--year', help='Accident Year', type=int, required=True)

    args = vars(parser.parse_args())

    DataUploader(**args).main()
