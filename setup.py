# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

"""
setup module for dkms-transfer-python2.

Created on 05/23/2022

@author: Alibaba Cloud SDK
"""

packages = find_packages()
NAME = "alibabacloud-dkms-transfer-python2"
DESCRIPTION = "Alibaba Cloud Dedicated KMS Transfer SDK for Python2"
AUTHOR = "Alibaba Cloud SDK"
AUTHOR_EMAIL = "sdk-team@alibabacloud.com"
URL = "https://github.com/aliyun/alibabacloud-dkms-transfer-python2-sdk"
VERSION = "0.0.3"
REQUIRES = [
    "alibabacloud_dkms_gcs_python2>=0.0.5",
    'aliyun_python_sdk_core>=2.13.30',
    'aliyun_python_sdk_kms>=2.14.0',
]

LONG_DESCRIPTION = ''
if os.path.exists('./README.rst'):
    with open("./README.rst") as fp:
        LONG_DESCRIPTION = fp.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License 2.0",
    url=URL,
    keywords=["alibabacloud", "dkms-transfer-sdk"],
    packages=find_packages(exclude=["example*"]),
    include_package_data=True,
    platforms="any",
    install_requires=REQUIRES,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development"
    )
)
