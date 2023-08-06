#!/usr/bin/env python

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

# Non-qualified import of `versioneer`; local file is intended
import versioneer

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ALS.Liam',  # Required

    version=versioneer.get_version(),  # Required

    cmdclass=versioneer.get_cmdclass(),  # Required

    description='Visualize CCD data from ALS BL 4.0.2 diffractometer',  # Required

    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',

    url='https://bitbucket.org/berkeleylab/als.liam/src/master/',  # Optional

    author='Padraic Shafer',  # Optional
    author_email='pshafer@lbl.gov',  # Optional

    classifiers=[  # Optional

        'Development Status :: 4 - Beta',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',

        # 'License :: OSI Approved :: BSD License :: BSD-3-Clause-LBNL',
        'License :: OSI Approved :: BSD License', # 'BSD-3-Clause-LBNL'

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

        'Operating System :: OS Independent',
        'Environment :: Console',
    ],

    keywords='CCD RSXD x-ray ALS BL4.0.2 diffraction',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=[
        'PkgScript',
        'ALS.Milo',
        'pyqtgraph',
        ],  # Optional

    extras_require={  # Optional
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },

    include_package_data=True,

    entry_points={  # Optional
        'console_scripts': [
            'fitsViewer=als.liam.fitsViewer:main',
            # 'liam=als.liam.fitsViewer:main',
        ],
    },
)