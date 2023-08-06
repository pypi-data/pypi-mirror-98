# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup

if not os.environ.get('__ALIAS_PACKAGE__01234__lalalalallal__'):
    sys.exit('Oops! The real package name is "huskar-sdk-v2". please install "huskar-sdk-v2".')  # noqa

setup(
    name="huskar-sdk",
    version="0.1.0",
    url="https://pypi.org/project/huskar-sdk-v2/",
    long_description="""Use `huskar-sdk-v2 <https://pypi.org/project/huskar-sdk-v2/>`_ instead.""",    # noqa
    install_requires=['huskar-sdk-v2'],
    classifiers=[],
)
