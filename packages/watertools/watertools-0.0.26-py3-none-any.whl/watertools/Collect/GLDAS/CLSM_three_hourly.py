# -*- coding: utf-8 -*-
import sys
from watertools.Collect.GLDAS.CLSM_DataAccess import DownloadData


def main(Dir, Vars, Startdate, Enddate, latlim, lonlim, Periods=[1, 2, 3, 4, 5, 6, 7, 8], cores=False, Waitbar = 1):
    """
    This function downloads GLDAS CLSM three-hourly data for a given variable, time
    interval, spatial extent, and day period.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Var --  ['wind','qair'] Variable code. Run: VariablesInfo('day').descriptions.keys()
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    Periods -- List of numbers from 1 to 8 (e.g. [1,4,5,8]). Stands for the
               period of hour of a day as follows:
                    Period       Hours
                      1      00:00 - 03:00
                      2      03:00 - 06:00
                      3      06:00 - 09:00
                      4      09:00 - 12:00
                      5      12:00 - 15:00
                      6      15:00 - 18:00
                      7      18:00 - 21:00
                      8      21:00 - 24:00
    Waitbar -- 1 (Default) Will print a waitbar

    """
    for Var in Vars:

        if Waitbar == 1:
            print('\nDownloading three hourly GLDAS CLSM %s data for the period %s till %s' %(Var, Startdate, Enddate))

        # Download data
        DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, Waitbar, cores, TimeCase='three_hourly', CaseParameters=Periods)

if __name__ == '__main__':
    main(sys.argv)

