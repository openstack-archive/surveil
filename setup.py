import setuptools
from setuptools import find_packages

setuptools.setup(
    setup_requires=['pbr'],
    pbr=True,
    packages=find_packages(exclude=['ez_setup'])
)
