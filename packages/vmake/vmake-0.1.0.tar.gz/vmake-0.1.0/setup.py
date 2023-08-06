#!/usr/bin/env python3
"""
SPDX-License-Identifier: BSD-3-Clause
This file is part of vmake, https://github.com/patrislav1/vmake
Copyright (C) 2020 Patrick Huesmann <info@patrick-huesmann.de>
"""

import setuptools
from pathlib import Path as path

readme_contents = path('./README.md').read_text()
requirements = path('./requirements.txt').read_text().splitlines()
packages=setuptools.find_packages(include=['vmake'])

setuptools.setup(
    name='vmake',
    version='0.1.0',
    author='Patrick Huesmann',
    author_email='info@patrick-huesmann.de',
    url='https://github.com/patrislav1/vmake',
    license='BSD',
    description='Wrapper for \"make\", creating VSCode hyperlinks',
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    keywords='vscode make gcc hyperlinks',
    install_requires=requirements,
    packages=packages,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ],
    entry_points={
        'console_scripts': [
            'vmake=vmake.vmake:main',
        ],
    },
    python_requires='>=3.6'
)
