import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass

import urllib.request

import logging

logger = logging.getLogger(__name__)

@dataclass
class DataScraper(object):
    '''
    Simple data scraper to extract data from: https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_since_1932.txt
    Perform post processing on data to obtain hourly timeseries.
    '''

    _url: str = 'https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_since_1932.txt'


    def load_data(self, st_date: datetime = datetime(1932, 1, 1, 0), en_date: datetime = datetime.now(), data_quality_filter: tuple = (0,1,2)) -> pd.DataFrame:
        '''Load data from txt file and parse values into pandas data frame'''

        self.data_quality_filter = data_quality_filter

        raw_df = self._load_raw_data()
        df = self._preprocess(raw_df)
        df = self._interpolate(df)

        # filter date
        df = df.loc[st_date:en_date, :]

        return df



    def _load_raw_data(self) -> pd.DataFrame:

        # read txt
        raw_list = urllib.request.urlopen(self._url).read()
        raw_list = raw_list.decode('utf-8').split('\n')

        # parse columns
        columns = raw_list[29][1:].split()

        # print source
        self._print_source(raw_list)

        # drop row starting with #
        raw_list = [x for x in raw_list if not x.startswith('#')]

        # parse row
        raw_df = [self._parse_raw(r) for r in raw_list]
        raw_df = pd.DataFrame(raw_df, columns = columns)
        raw_df.dropna(inplace=True)

        final_columns = ['YYY', 'MM', 'DD', 'hh.h', 'Kp', 'ap', 'D']
        raw_df = raw_df.loc[:, final_columns]

        # format columns
        raw_df.loc[:, ['Kp']] = raw_df.loc[:, ['Kp']].astype(float)
        raw_df.loc[:, ['hh.h']] = raw_df.loc[:, ['hh.h']].astype(float).astype(int)
        raw_df.loc[:, ['YYY', 'MM', 'DD', 'D']] = raw_df.loc[:, ['YYY', 'MM', 'DD', 'D']].astype(int)

        # valuedate column and set index
        raw_df['valuedate'] = [datetime(y, m, d, h) for (y,m,d,h) in list(raw_df.iloc[:, 0:4].itertuples(index =False))]
        raw_df = raw_df.set_index('valuedate')

        raw_df.rename(columns = {'YYY': 'year', 'MM': 'month', 'DD': 'day', 'hh.h': 'hour'}, inplace = True)

        return raw_df

    @staticmethod
    def _parse_raw(r):
        parsed_r = r.split()
        return parsed_r


    @staticmethod
    def _print_source(raw_df):
        print('-------------------  DATA SOURCE -------------------')
        print('\n'.join(raw_df[1:5]))
        print('----------------------------------------------------')



    def _interpolate(self, df):
        '''Interpolate to hourly timeseries'''

        df = df.resample('H').mean()
        df = df.interpolate(method = 'cubic')
        df = df.clip(0) # Make sure no negative values have been introduced during interpolation
        return df


    def _preprocess(self, df):
        '''Clean data'''

        # only definitive values
        df = df.loc[df['D'].isin(self.data_quality_filter)]

        # drop Kp = -1 (i.e. missing values)
        df = df.query('Kp>=0')

        # drop useless columns
        df = df[['Kp', 'ap']]

        df = df.astype(float)

        return df


if __name__ == '__main__':

    data_scraper = DataScraper()
    data = data_scraper.load_data()

    data.loc[datetime(2020, 1, 1):, :]