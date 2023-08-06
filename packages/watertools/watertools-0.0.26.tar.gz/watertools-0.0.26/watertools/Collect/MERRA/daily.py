# -*- coding: utf-8 -*-
import sys
from watertools.Collect.MERRA.DataAccess import DownloadData


def main(Dir, Vars, Startdate, Enddate, latlim, lonlim, Waitbar = 1, data_type = ["mean"]):
    """
    This function downloads MERRA daily data for a given variable, time
    interval, and spatial extent.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Vars -- ['t2m', 'v2m'] 
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    Waitbar -- 1 (Default) Will print a waitbar
    """
    for Var in Vars:

        if Waitbar == 1:
            print('\nDownloading daily MERRA %s data for the period %s till %s' %(Var, Startdate, Enddate))

        # Download data
        DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, "daily", '', Waitbar, data_type)

if __name__ == '__main__':
    main(sys.argv)
