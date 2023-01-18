# coding: utf-8
from setuptools import setup


setup(
    name="aocutils",
    version='0.0.1',
    author="sir_Gollum",
    description=(
        "A library of helpers for solving Advent of Code problems."
    ),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ],
    packages=['aocutils'],
    package_dir={'aocutils': 'aocutils'},
    install_requires=(
        'pytest>=3X',
        'tqdm',
    )
)
