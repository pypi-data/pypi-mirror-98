# -*- coding: utf-8 -*-
'''
Authors: Tim Hessels
Module: Collect/GLEAM
'''

import sys
from watertools.Collect.GLEAM.DataAccess import DownloadData


def main(Dir, Startdate, Enddate, latlim, lonlim, cores=False, Waitbar = 1):
    """
    This function downloads GLEAM daily data for the specified time
    interval, and spatial extent.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
	 cores -- amount of cores used
    Waitbar -- 1 (Default) will print a waitbar
    """
    TimeCase = 'daily'
    if Waitbar == 1:
        print('\nDownload daily GLEAM ET data for the period %s till %s' %(Startdate, Enddate))

    DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar, cores, TimeCase, Product = "ET")

if __name__ == '__main__':
    main(sys.argv)