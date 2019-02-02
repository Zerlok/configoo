#!/usr/bin/env python3.7

from pathlib import Path
from setuptools import setup, find_packages

SETUP_FILE = Path(__file__)
PROJECT_DIR = SETUP_FILE.parent

LIB_NAME = 'configoo'


def load_text(path: Path) -> str:
    with path.open('r') as fd:
        return fd.read()


setup(
    name=LIB_NAME,
    version='0.0.3',
    description='Python config lib for loading application configurations',
    long_description=load_text(PROJECT_DIR / 'README.md'),
    long_description_content_type='text/markdown',
    author='Danil Troshnev',
    author_email='denergytro@gmail.com',
    url=f'https://bitbucket.org/Zerlok/{LIB_NAME}/',
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    install_requires=[
    ],
    extras_require={
        'env': [],
        'dotenv': [
            'python-dotenv >= 0.10.1',
        ],
        'json': [],
    },
)
