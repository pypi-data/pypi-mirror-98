# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages
from setuptools import setup

# obtain version string from __init__.py
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'integrators', '__init__.py'), 'r') as f:
    init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README and CHANGES
README = '''
'''

# setup
setup(
    name='integrators',
    version=version,
    description='Integrators: A backend-free numerical integration library for differential equations',
    long_description=README,
    author='Chaoming Wang',
    author_email='adaduo@outlook.com',
    packages=find_packages(exclude=['docs*', 'develop*', ]),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.15',
        'numba>=0.50.0',
    ],
    # url='https://github.com/PKU-NIP-Lab/BrainPy',
    keywords='computational-neuroscience '
             'differential-equations '
             'numerical-integration '
             'ordinary-differential-equations ODE '
             'stochastic-differential-equations SDE'
             'delay-differential-equations DDE'
             'fractional-differential-equations FDE',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
    ]
)
