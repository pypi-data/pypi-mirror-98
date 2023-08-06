# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Module: Collect/HiHydroSoil

Restrictions:
The data and this python file may not be distributed to others without
permission of the WA+ team due data restriction of the HiHydroSoil developers.

Description:
This module downloads HiHydroSoil data from
ftp.wateraccounting.unesco-ihe.org. Use the HiHydroSoil function to
download and create monthly HiHydroSoil images in Gtiff format.

Examples:
from watertools.Collect import HiHydroSoil
HiHydroSoil.ThetaSat_TopSoil(Dir='C:/Temp/',  latlim=[-10, 30], lonlim=[-20, -10])
"""

from .ThetaSat_TopSoil import main as ThetaSat_TopSoil

__all__ = ['monthly']

__version__ = '0.1'
