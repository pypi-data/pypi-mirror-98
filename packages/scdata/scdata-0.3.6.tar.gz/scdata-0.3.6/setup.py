# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

import sys

if sys.version_info < (3,0):
    sys.exit("scdata requires python 3.")

PROJECT_URLS = {
    "Documentation": "https://docs.smartcitizen.me/Data%20Analysis/",
    "Source Code": "https://github.com/fablabbcn/smartcitizen-data",
}    

setup(
    name='scdata',
    version= '0.3.6',
    description='Analysis of sensors and time series data',
    author='oscgonfer',
    license='GNU-GPL3.0',
    packages=find_packages(),
    keywords=['air', 'sensors', 'Smart Citizen'],
    url='https://github.com/fablabbcn/smartcitizen-data',
    project_urls=PROJECT_URLS,
    long_description = ("""
        ## scdata - Analysis of sensors and time series data

        `scdata` is a **sensor data analysis framework** built with the purpose of *analysis*, 
        *calibration* and *post-processing* of sensor data. It is particularly 
        focused on sensors for environmental monitoring such as the low-cost sensors in the 
        [Smart Citizen Project](https://www.smartcitizen.me). As such provides
        tools for workflow automation and sensor calibration.

        It aims to unify several sources of data and to provide tools for analysing data by:

        * Interacting with several sensors APIs
        * Clean data, export and calculate metrics
        * Model sensor data and calibrate sensors
        * Generate data visualisations

    """),

    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],

    install_requires=[  'attrs~=20.3.0',
                        'branca==0.4.0',
                        'certifi~=2020.12.5',
                        'chardet==3.0.4',
                        'cycler==0.10.0',
                        'Flask~=1.1.2',
                        'folium==0.11.0',
                        'geographiclib==1.50',
                        'geopy==1.21.0',
                        'idna==2.9',
                        'importlib-metadata~=1.7.0',
                        'Jinja2==2.11.2',
                        'kiwisolver==1.2.0',
                        'MarkupSafe==1.1.1',
                        'matplotlib==3.2.1',
                        'numpy~=1.19.4',
                        'pandas~=1.0.3',
                        'pdfrw==0.4',
                        'PDPbox==0.2.0',
                        'plotly~=4.14.3',
                        'pyparsing==2.4.7',
                        'python-dateutil==2.8.1',
                        'pytz==2020.1',
                        'PyYAML==5.3.1',
                        'requests==2.23.0',
                        'reportlab==3.5.*',
                        'scipy==1.4.1',
                        'scikit-learn==0.23.1',
                        'seaborn==0.10.1',
                        'Shapely==1.7.0',
                        'six==1.14.0',
                        'termcolor==1.1.0',
                        'tqdm~=4.50.2',
                        'tzwhere==3.0.3',
                        'urllib3==1.25.9',
                        'webencodings==0.5.1',
                        'zipp==3.1.0'],

    setup_requires=['wheel'],

    include_package_data=True,
    zip_safe=False
)
