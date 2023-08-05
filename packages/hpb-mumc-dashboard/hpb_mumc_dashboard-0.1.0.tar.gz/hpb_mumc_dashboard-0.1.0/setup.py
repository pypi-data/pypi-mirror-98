#!/usr/bin/env python

import os

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pytest', 'bokeh', 'django']

setup_requirements = []

test_requirements = []

setup(
    author="Ralph Brecheisen",
    author_email='r.brecheisen@maastrichtuniversity.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='hpb_mumc_dashboard',
    name='hpb_mumc_dashboard',
    packages=find_packages(include=['hpb_mumc_dashboard', 'hpb_mumc_dashboard.*']),
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'hmd.etl=hpb_mumc_dashboard.etl.script_runner:main',
            # 'hmd.dashboard=hpb_mumc_dashboard.dashboard.server_app:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/hpb_mumc_dashboard',
    version=os.environ['VERSION'],
    zip_safe=False,
)
