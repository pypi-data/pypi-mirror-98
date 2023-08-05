from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1dev1'
DESCRIPTION = 'Aerodynamics Functions for Engineers and Scientists'
LONG_DESCRIPTION = 'A package for Aerodynamics Engineers and Scientists that enables them to use various numerical methods, unit conversions, useful functions and needed constants'

# Setting up
setup(
    name="aerodynamics",
    version=VERSION,
    author="Skyworks (Dilara Ozev, Ethem Yılmaz)",
    author_email="<dilarassdh@hotmail.com>,<ethemymz54@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    
    packages=find_packages(),
    install_requires=['numpy','matplotlib'],
    keywords=['python', 'numerical_methods', 'aerodynamics', 'aircrafts', 'rockets', 'mathematical_functions','aerospace','aeronautics', 'reinforcement learning'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
