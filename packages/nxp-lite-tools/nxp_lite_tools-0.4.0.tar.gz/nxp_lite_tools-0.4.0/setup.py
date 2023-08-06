#!/usr/bin/env python3
#-*-coding:utf-8-*-

from setuptools import setup, find_packages

metadata = {}
about_file = "nxp_lite_tools/__about__.py"
try:
    execfile(about_file, metadata)
except:
    with open(about_file, encoding="utf-8") as fp:
        exec(fp.read(), metadata)

setup(
    name="nxp_lite_tools",
    version=metadata["__version__"],
    description=metadata["__description__"],
    long_description=metadata["__long_description__"],
    long_description_content_type=metadata["__long_description_content_type__"],
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    license=metadata["__license__"],

    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],

    entry_points={
        'console_scripts': [
            'nxp_lite_tools = nxp_lite_tools:main',
        ]
    },

    extras_require={
        'pb': ['nxp_pb'],
        'lf': ['nxp_lf'],
        'pp': ['nxp_pp'],
        'ls': ['nxp_ls'],
    },

    package_data={'': ['help']},
)
