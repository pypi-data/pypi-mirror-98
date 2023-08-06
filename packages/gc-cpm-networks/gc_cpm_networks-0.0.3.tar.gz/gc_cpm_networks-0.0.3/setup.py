#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='gc_cpm_networks',
    version='0.0.3',
    description='Global Context Convolutional Pose Machine Network',
    author='Kacper Kulczak',
    author_email='k.kulczak@xberry.tech',
    packages=find_packages(),
    url='https://github.com/xBerryOS/gccpm-look-into-person-cvpr19.pytorch',
    python_requires=">=3.8.*",
)
