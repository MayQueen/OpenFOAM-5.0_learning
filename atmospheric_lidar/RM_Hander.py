import os,sys
sys.path.append('C:\\Users\\MERI\\Desktop\\atmospheric_lidar')

import glob
from raymetrics import ScanningLidarMeasurement

LidarDataObject= r'C:\\Users\\MERI\\Desktop\\20190120\\RM1912000.021110'

RM_file = ScanningLidarMeasurement(file_path)