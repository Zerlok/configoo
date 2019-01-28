#!/usr/bin/env python3.7

from setuptools import setup, find_packages

LIB_NAME = 'configoo'


setup(
    name=LIB_NAME,
    version='0.0.1',
    description='Python config lib for loading application configurations',
    author='Danil Troshnev',
    author_email='denergytro@gmail.com',
    url=f'https://bitbucket.org/Zerlok/{LIB_NAME}/',
    packages=[
        '.'.join((
            LIB_NAME,
            package,
        ))
        for package in find_packages('src')
    ],
    package_dir={
        LIB_NAME: 'src',
    },
    install_requires=[
        
    ],
    extras_require={

    },
)
