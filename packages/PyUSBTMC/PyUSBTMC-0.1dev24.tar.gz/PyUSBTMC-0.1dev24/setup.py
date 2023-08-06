#!/usr/bin/env python
"""
"""
import os,platform,re,sys

extra=dict()
if sys.version_info >= (3,):
    extra['use_2to3'] = True

from distutils.core import setup
from distutils.extension import Extension

#from Cython.Distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext



try:
   from distutils.command.build_py import build_py_2to3 as build_py #for Python3
except ImportError:
   from distutils.command.build_py import build_py     # for Python2

rev="$Revision: 0.1dev24$"
sysname=platform.system()
HGTag = "$HGTag: null.9-13a5a1ebeb21 $"
HGTagShort="$HGTagShort: null.9 $"
HGdate="$HGdate: Sun, 20 May 2018 13:12:01 +0900 "
HGLastLog="$lastlog: add /usr/share/hwdata to search-path for usb.ids $"
HGcheckedIn="$checked in by: Noboru Yamamoto <noboru.yamamoto@kek.jp> $"

setup(name="PyUSBTMC",
      version=rev[11:-1],
      author="Noboru Yamamoto, KEK, JAPAN",
      author_email = "Noboru.YAMAMOTO@kek.jp",
      description ="Python module to control USBTMC/USB488 from python",
      long_description=""" Python module to control USBTMC/USB488 from python.
It requires pyusb module and libusb (or openusb) library to run. 
Although it is still in the development stage, it can read/write data from/to the devices.""",
      platforms="tested on MacOSX10.7",
      url="http://www-acc.kek.jp/EPICS_Gr/products/",
      py_modules=["PyUSBTMC","lsusb","usbids","samples.test_DPO", "samples.test_dso_anim"],
      data_files=[("share/misc",['usb.ids'])],
      ext_modules=cythonize([
          Extension("cPyUSBTMC", ["cPyUSBTMC.pyx"]),
          ]),
      )
