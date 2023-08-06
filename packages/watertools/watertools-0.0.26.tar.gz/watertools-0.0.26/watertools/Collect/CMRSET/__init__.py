# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Module: Collect/CMRSET

Restrictions:
The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the CMRSET developers.

Description:
This module downloads CMRSET data from
ftp.wateraccounting.unesco-ihe.org. Use the CMRSET.monthly function to
download and create monthly CMRSET images in Gtiff format.
The data is available between 2000-01-01 till 2012-12-31.

Examples:
from watertools.Collect import CMRSET
CMRSET.monthly(Dir='C:/Temp/', Startdate='2008-12-01', Enddate='2011-01-20',
           latlim=[-10, 30], lonlim=[-20, -10])
"""

from .monthly import main as monthly

__all__ = ['monthly']

__version__ = '0.1'
