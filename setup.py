#!/usr/bin/env python3.7

from setuptools import setup, find_packages

install_requires = [
    'boto3',
    'sanic',
    'hbmqtt',
    'uvloop',
    'jinja2'
]

setup(
    name='ambiance',
    version='1.0',
    description='',
    author='M. Barry McAndrews',
    author_email='bmcandrews@pitt.edu',
    requires=install_requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ambiance = ambiance.__main__:main'
        ]
    }
)
