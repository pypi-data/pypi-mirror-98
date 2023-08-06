# -*- coding: utf-8 -*-
import sys
from watertools.Collect.GLDAS.DataAccess import DownloadData


def main(Dir, Vars, Startdate, Enddate, latlim, lonlim, cores=False,
         SumMean=1, Min=0, Max=0, Waitbar = 1, gldas_version = '2.1'):
    """
    This function downloads GLDAS daily data for a given variable, time
    interval, and spatial extent.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Vars -- ['wind_f_inst','qair_f_inst'] (array of strings) Variable code: VariablesInfo('day').descriptions.keys()
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    SumMean -- 0 or 1. Indicates if the output values are the daily mean for
               instantaneous values or sum for fluxes
    Min -- 0 or 1. Indicates if the output values are the daily minimum
    Max -- 0 or 1. Indicates if the output values are the daily maximum
    Waitbar -- 1 (Default) Will print a waitbar
    gldas_version = '2.1' (Default) or '2.0'

    Version 2.1 is available from 2000-01-01 till present
    Version 2.0 is available from 1948-01-01 till 2010-12-31
    """
    for Var in Vars:

        if Waitbar == 1:
            print('\nDownloading daily GLDAS %s data for the period %s till %s' %(Var, Startdate, Enddate))

        # Download data
        DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, Waitbar, cores,
					 TimeCase='daily', CaseParameters=[SumMean, Min, Max], gldas_version = gldas_version)

if __name__ == '__main__':
    main(sys.argv)

