#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

from bapy import setup_bapy
from bapy import __version__

setup(
    author=setup_bapy.gecos,
    author_email=setup_bapy.email,
    description=setup_bapy.description,
    entry_points={
        'console_scripts': [
            f'{setup_bapy.repo} = {setup_bapy.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=setup_bapy.requirements['requirements'],
    name=setup_bapy.repo,
    package_data={
        setup_bapy.repo: [f'{setup_bapy.repo}/scripts/*', f'{setup_bapy.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.9,<4',
    scripts=setup_bapy.scripts_relative,
    setup_requires=setup_bapy.requirements['requirements_setup'],
    tests_require=setup_bapy.requirements['requirements_test'],
    url=setup_bapy.url.url,
    use_scm_version=False,
    version=__version__,
    zip_safe=False,
)
