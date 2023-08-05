#!/usr/bin/env python3
from setuptools import setup, find_packages
from glob import glob
import versioneer


desc = """
pyts2: Next-generation utilities and a python library for manipulating
timelapses in the TimeStream format
"""

with open("requirements.txt") as fh:
    install_requires = [req.strip() for req in fh]

test_requires = [
    "pytest",
    "pytest-cov",
    "pytest-remotedata",
]


setup(
    name="pyts2",
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=install_requires,
    tests_require=test_requires,
    include_package_data=True,
    description=desc,
    entry_points='''
        [console_scripts]
        tstk=pyts2.commandline:tstk_main
    ''',
    author="Kevin Murray",
    author_email="foss@kdmurray.id.au",
    url="https://gitlab.com/appf-anu/pyts2",
    keywords=["timestream", "timelapse", "photography", "video"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        ],
    test_suite="tests",
    )
