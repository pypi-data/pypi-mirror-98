import setuptools
import os
from setuptools import setup

from os import path
#this_directory = path.abspath(path.dirname(__file__))
#with open(path.join(this_directory, 'README.md')) as f:
with open("README.md", "r") as f:
    long_description = f.read()
	

with open("requirements.txt","r") as f:
    required = f.read().splitlines()
    
setuptools.setup(
    name='maads',
    version='5.01',
    description='Multi-Agent Accelerator for Data Science (MAADS)',
    license='OTICS Advanced Analytics Inc.',
    packages=['maads'],
    author='Sebastian Maurice',
    author_email='sebastian.maurice@otics.ca',
    keywords=['multi-agent, data science, optimization, prescriptive analytics, machine learning, automl,auto-ml,artificial intelligence', 'predictive analytics', 'advanced analytics'],
    long_description=long_description,
    install_requires=required,
    long_description_content_type='text/markdown',
    url='https://github.com/smaurice101/acnsmauricedsmas'
)

