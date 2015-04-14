"""This is the setup file used when creating a PyPI package of this project"""
from setuptools import setup  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CPUC_NetworkTest_Parser',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.6',

    description='A Python object for parsing iperf Network Testing output',
    long_description=long_description,

    # The project's main homepage.
    url='http://pwalker91.github.io/CSUMB_CPUC-Test-Parser/',

    # Author details
    author='Peter Walker',
    author_email='pwalker@csumb.edu',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',

        #The language this project is written in
        'Natural Language :: English',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        #The intended operating systems
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='csumb text processing data network testing information analysis',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['FileParser','csvGeneration'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    #install_requires=['Pillow', 'numpy'],
)
