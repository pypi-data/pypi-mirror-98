#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import chain
import os
import os.path
import shutil
import sys

from setuptools import find_packages
from setuptools import setup

pkg_name = "tsgettoolbox"
version = open("VERSION").readline().strip()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")

    # The following block of code is to set the timestamp on files to
    # 'now', otherwise ChromeOS/google drive sets to 1970-01-01 and then
    # no one can install it because zip doesn't support dates before
    # 1980.
    os.chdir("dist")
    os.system("tar xvzf {pkg_name}-{version}.tar.gz".format(**locals()))
    os.system("find {pkg_name}-{version}* -exec touch {{}} \\;".format(**locals()))
    os.system(
        "tar czf {pkg_name}-{version}.tar.gz {pkg_name}-{version}".format(**locals())
    )
    shutil.rmtree("{pkg_name}-{version}".format(**locals()))
    os.chdir("..")

    os.system("twine upload dist/{pkg_name}-{version}.tar.gz".format(**locals()))
    sys.exit()

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    "appdirs",
    "beautifulsoup4",
    "future",
    "geojson",
    "isodate",
    "lxml",
    "mechanize",
    "numpy >= 1.7",
    "pandas >= 0.15.0",
    "pytest",
    "requests",
    "suds-jurko",
    "tables",
    "tstoolbox >= 102, < 103",
    "zeep",
]


setup(
    name="tsgettoolbox",
    version=version,
    description="Will get time series from different sources on the internet.",
    long_description=README,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="time_series uri url web_services rest",
    author="Tim Cera, P.E.",
    author_email="tim@cerazone.net",
    url="http://timcera.bitbucket.io/tsgettoolbox/docsrc/index.html",
    packages=find_packages(),
    package_data={"tsgettoolbox": ["tsgettoolbox/services/usgs/*.dat"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["tsgettoolbox=tsgettoolbox.tsgettoolbox:main"]},
    test_suite="tests",
    python_requires=">=3.7.1",
)
