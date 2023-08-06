# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Contact: timhessels@hotmail.com
Repository: https://github.com/TimHessels/watertools
Module: Collect/CHIRPS

Description:
This module downloads daily and monthly CHIRPS 2.0 data from
ftp://chg-ftpout.geog.ucsb.edu server. Use the CHIRPS.daily or CHIRPS.monthly
functions to download and create daily or monthly CHIRPS images in Gtiff
format. The CHIRP data is available since 1981-01-01 till the present.

Examples:
from watertools.Collect import CHIRPS
CHIRPS.daily(Dir='C:/Temp/', Startdate='1999-02-01', Enddate='1999-02-03',
             latlim=[-10, 30], lonlim=[-20, 120])
CHIRPS.monthly(Dir='C:/Temp/', Startdate='1999-02-01', Enddate='1999-02-28',
               latlim=[-10, 30], lonlim=[-20, 120])
"""

from .daily import main as daily
from .monthly import main as monthly

__all__ = ['daily', 'monthly']

__version__ = '0.1'
