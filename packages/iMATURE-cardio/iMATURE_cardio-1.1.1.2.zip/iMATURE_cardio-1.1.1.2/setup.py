import sys
import os
from setuptools import setup, find_packages

setup(
    # Module name (lowercase)
    name='iMATURE_cardio',
    version='1.1.1.2',
    description='iMATURE_cardio',
    url='http://www.jordiheijman.net/',

    # Packages to exclude
    packages=find_packages(),
    zip_safe=False,

    # List of dependencies
    install_requires=[
        'myokit',
        #'PyQt5',
    ],

    # Register as a shell script
    entry_points = {
        'console_scripts': [
            'iMATURE = iMATURE_cardio.__main__:main',
        ],
    },

    # Include non-python files (via MANIFEST.in)
    include_package_data=True,
)
