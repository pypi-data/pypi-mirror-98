#!/usr/bin/env python

"""
suanpan
"""


import itertools
import os
import re

from setuptools import find_packages, setup

VERSION_PARRTERN = r"__version__ = \"([\d\w\.]*)\""
VERSION_FILE = os.path.join("suanpan", "__init__.py")
VERSION = re.findall(VERSION_PARRTERN, open(VERSION_FILE, "r").read())[0]

BASE_REQUIRES = [
    "six>=1.13.0",
    "imageio>=2.4.1",
    "numpy>=1.16.2",
    "opencv-python-headless>=4.1.2",
    "pandas>=0.23.4,<1.0",
    "tqdm>=4.28.1",
    "retrying>=1.3.3",
    "pyodps>=0.8.0",
    "tabulate>=0.8.3",
    "colorama>=0.4.1",
    "lostc>=0.1.0",
    "addict>=2.2.0",
    "timeout-decorator>=0.4.1",
    "xlwt>=1.3.0",
    "openpyxl>=3.0.2",
    "xlrd>=1.0.0",
    "gevent>=20.5.0",
    "python-socketio==4.6.1",
    "gevent-websocket>=0.10.1",
    "wsaccel>=0.6.2",
    "ujson>=2.0.3",
    "pytz>=2020.1",
]
OSS2_REQUIRES = ["oss2>=2.9.1"]
MINIO_REQUIRES = ["minio==7.0.0"]
REDIS_REQUIRES = ["redis>=3.2.0"]
MYSQL_REQUIRES = ["mysql-connector-python>=8.0.16"]
POSTGRES_REQUIRES = ["psycopg2-binary>=2.8.2"]
HIVE_REQUIRES = [
    "sasl>=0.2.1",
    "thrift-sasl>=0.3.0",
    "thrift>=0.11.0",
    "pyhive[hive]>=0.6.1",
]
ZMQ_REQUIRES = ["pyzmq>=18.1.0"]
INSTALL_REQUIRES = list(
    itertools.chain(
        BASE_REQUIRES,
        OSS2_REQUIRES,
        MINIO_REQUIRES,
        REDIS_REQUIRES,
        MYSQL_REQUIRES,
        POSTGRES_REQUIRES,
        HIVE_REQUIRES,
        ZMQ_REQUIRES,
    )
)
README = "README.md"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


fix_packages = ["__suanpan__"]
packages = find_packages(exclude=["tests"])
packages.extend(fix_packages)

setup(
    name="suanpan",
    version=VERSION,
    packages=packages,
    license="See License",
    author="majik",
    author_email="me@yamajik.com",
    description="Suanpan SDK",
    long_description=read_file(README),
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
