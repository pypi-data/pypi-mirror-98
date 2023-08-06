# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Module: Collect/SEBS

Restrictions:
The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the SEBS developers.

Description:
This script collects SEBS data from the UNESCO-IHE FTP server. The data has a
monthly temporal resolution and a spatial resolution of 0.01 degree. The
resulting tiff files are in the WGS84 projection.
The data is available between 2000-03-01 till 2015-12-31.

Example:
from watertools.Collect import SEBS
SEBS.monthly(Dir='C:/Temp/', Startdate='2003-02-24', Enddate='2003-03-09',
                     latlim=[50,54], lonlim=[3,7])

"""
# General modules
import numpy as np
import os
import pandas as pd
from ftplib import FTP
import scipy.io as spio

# Water Accounting Modules
import watertools
import watertools.General.data_conversions as DC

def DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar):
    """
    This scripts downloads SEBS ET data from the UNESCO-IHE ftp server.
    The output files display the total ET in mm for a period of one month.
    The name of the file corresponds to the first day of the month.

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'
    lonlim -- [ymin, ymax] (values must be between -90 and 90)
    latlim -- [xmin, xmax] (values must be between -180 and 180)
    """
    # Check the latitude and longitude and otherwise set lat or lon on greatest extent
    if latlim[0] < -90 or latlim[1] > 90:
        print('Latitude above 90N or below -90S is not possible. Value set to maximum')
        latlim[0] = np.max(latlim[0], -90)
        latlim[1] = np.min(latlim[1], 90)
    if lonlim[0] < -180 or lonlim[1] > 180:
        print('Longitude must be between 180E and 180W. Now value is set to maximum')
        lonlim[0] = np.max(lonlim[0],-180)
        lonlim[1] = np.min(lonlim[1],180)

	# Check Startdate and Enddate
    if not Startdate:
        Startdate = pd.Timestamp('2000-01-01')
    if not Enddate:
        Enddate = pd.Timestamp('2017-06-30')

    # Creates dates library
    Dates = pd.date_range(Startdate, Enddate, freq = "MS")

    # Create Waitbar
    if Waitbar == 1:
        import watertools.Functions.Random.WaitbarConsole as WaitbarConsole
        total_amount = len(Dates)
        amount = 0
        WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # Define directory and create it if not exists
    output_folder = os.path.join(Dir, 'Evaporation', 'SEBS', 'Monthly')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for Date in Dates:

        # Define year and month
        year = Date.year
        month = Date.month

        # Date as printed in filename
        Filename_out= os.path.join(output_folder,'ETa_SEBS_mm-month-1_monthly_%s.%02s.%02s.tif' %(Date.strftime('%Y'), Date.strftime('%m'), Date.strftime('%d')))

        # Define end filename
        Filename_in = os.path.join("ETm%d%02d.mat" %(year, month))

		 # Temporary filename for the downloaded global file
        local_filename = os.path.join(output_folder, Filename_in)

        # Download the data from FTP server if the file not exists
        if not os.path.exists(Filename_out):
            try:
                Download_SEBS_from_WA_FTP(local_filename, Filename_in)

                # Clip dataset
                Clip_Dataset(local_filename, Filename_out, latlim, lonlim)
                os.remove(local_filename)

            except:
                print("Was not able to download file with date %s" %Date)

        # Adjust waitbar
        if Waitbar == 1:
            amount += 1
            WaitbarConsole.printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    return

def Download_SEBS_from_WA_FTP(local_filename, Filename_in):
    """
    This function retrieves SEBS data for a given date from the
    ftp.wateraccounting.unesco-ihe.org server.

    Restrictions:
    The data and this python file may not be distributed to others without
    permission of the WA+ team due data restriction of the SEBS developers.

    Keyword arguments:
	 local_filename -- name of the temporary file which contains global SEBS data
    Filename_in -- name of the end file with the monthly SEBS data
    """

    # Collect account and FTP information
    username, password = watertools.Functions.Random.Get_Username_PWD.GET('FTP_WA')
    ftpserver = "ftp.wateraccounting.unesco-ihe.org"

    # Download data from FTP
    ftp=FTP(ftpserver)
    ftp.login(username,password)
    directory="/WaterAccounting_Guest/SEBS/Global_land_ET_V1/"
    ftp.cwd(directory)
    lf = open(local_filename, "wb")
    ftp.retrbinary("RETR " + Filename_in, lf.write)
    lf.close()

    return

def Clip_Dataset(local_filename, Filename_out, latlim, lonlim):

    # Open Dataset
    SEBS_Array = spio.loadmat(local_filename)['ETm']

    # Define area
    XID = [int(np.floor((180 + lonlim[0])/0.05)), int(np.ceil((180 + lonlim[1])/0.05))]
    YID = [int(np.ceil((90 - latlim[1])/0.05)), int(np.floor((90 -  latlim[0])/0.05))]

    # Define Georeference
    geo = tuple([-180 + 0.05*XID[0],0.05,0,90 - 0.05*YID[0],0,-0.05])

    # Clip Array
    SEBS_Array_clipped = SEBS_Array[YID[0]:YID[1], XID[0]:XID[1]] * 0.1

    # Save tiff file
    DC.Save_as_tiff(Filename_out, SEBS_Array_clipped, geo, "WGS84")
