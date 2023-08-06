# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Module: Collect/GLEAM

Description:
This module downloads GLEAM ET data from
www.gleam.eu. Use the GLEAM.ET_monthly function to
download and create monthly ET images in Gtiff format.

Examples:
from watertools.Collect import GLEAM
GLEAM.ET_monthly(Dir='C:/Temp3/', Startdate='2003-12-01', Enddate='2004-01-20',
           latlim=[20,30], lonlim=[30, 40])
from watertools.Collect import GLEAM
GLEAM.ET_daily(Dir='C:/Temp3/', Startdate='2003-12-01', Enddate='2004-01-20',
           latlim=[20,30], lonlim=[30, 40])

!!!!
You need a password to download this data. To get a password, you have to make an account here:  http://www.gleam.eu/#4
!!!!

"""

from .ET_monthly import main as ET_monthly
from .ET_daily import main as ET_daily
from .ETpot_monthly import main as ETpot_monthly
from .ETpot_daily import main as ETpot_daily

__all__ = ['ET_monthly', 'ET_daily', 'ETpot_monthly', 'ETpot_daily']

__version__ = '0.1'
