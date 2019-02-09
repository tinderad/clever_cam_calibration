from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='clever_cam_calibration',
    version='1.0',
    packages= ['clever_cam_calibration'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={'console_scripts':['calibrate_cam = clever_cam_calibration.clevercamcalib:calibrate_command',
                                     'calibrate_cam_ex = clever_cam_calibration.clevercamcalib:calibrate_ex_command']}
)
