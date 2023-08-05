# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 15:29:08 2021

@author: hp
"""
from setuptools import setup, find_packages
with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name='IFS_explorer',
    packages=find_packages(include=['IFS_explorer', 'IFS_explorer.*']),
    include_package_data = True,
    install_requires= ['matplotlib>=3.0,<4.0','numpy >=1.0,<2.0','astropy>=4.0,<5.0','opencv-python >=4.0,<5.0','scikit-image>=0.16.2,<1.0','scipy>=1.0,<2.0','Pillow >=7.0,<8.0'],
    version='1.0.2',
    description='A python3 interactive visualization tool for integral field spectroscopy data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/frosales258/IFS_explorer',
    author='Rosales-Ortega F. F., Angel Perez A., Xolo Tlapanco N.',
    author_email='frosales@cantab.net',
    license='MIT',
    classifiers=['Programming Language :: Python :: 3.8'], 
    keywords=['IFS', 'FITS Images', 'Astropy','3D cube'],
)
