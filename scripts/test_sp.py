#!/bin/python

from multiprocessing.spawn import import_main_path
import sys
sys.path.append("..")
import src.spatial_pattern as sp

import importlib
importlib.reload(sp)





