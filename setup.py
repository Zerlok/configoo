#!/usr/bin/env python3.7

from distutils.core import setup


setup(
    name='configlib',
    version='0.0.1',
    description='Python config lib for loading application configurations',
    author='Danil Troshnev',
    author_email='denergytro@gmail.com',
    url='https://bitbucket.org/Zerlok/configlib/',
    package_dir={
        'configlib': 'src',
    },
    packages=[
        'configlib',
        'configlib.field',
        'configlib.model',
        'configlib.loader',
    ],
)
