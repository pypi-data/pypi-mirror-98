# -*- coding: utf-8 -*-
import sys
from watertools.Collect.NLDAS.DataAccess import DownloadData


def main(Dir, Vars, Startdate, Enddate, latlim, lonlim, cores=False, Waitbar = 1, gldas_version = '2.1'):
    """
    This function downloads NLDAS monthly data for a given variable, time
    interval, and spatial extent.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Var --  ['tmp2m','spfh2m'] Variable code: VariablesInfo('day').descriptions.keys()
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    Waitbar -- 1 (Default) Will print a waitbar

    """
    for Var in Vars:

        if Waitbar == 1:
            print('\nDownloading monthly NLDAS NOAH %s data for the period %s till %s' %(Var, Startdate, Enddate))

        # Download data
        DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, Waitbar, cores,
                     TimeCase='monthly', CaseParameters=False)

if __name__ == '__main__':
    main(sys.argv)
