#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "randomwords",
    "google-api-python-client"
]

setup_requirements = [
]

test_requirements = [
]

dependency_links = [
]

setup(
    author="Ashley Williams",
    author_email='ashley.williams@pg.canterbury.ac.nz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Search functionality of COAST",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='coast_search',
    name='coast_search',
    packages=find_packages(include=['coast_search']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/zedrem/coast_search',
    version='0.0.1',
    zip_safe=False,
    dependency_links=dependency_links
)
