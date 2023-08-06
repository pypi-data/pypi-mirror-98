# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="os2mo-http-trigger-protocol",
    version="0.0.4",
    author="Magenta ApS",
    author_email="info@magenta.dk",
    description="Protocol library for OS2mo HTTP triggers",
    license="MPL 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.magenta.dk/rammearkitektur/os2mo-http-trigger-protocol",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pydantic',
    ],
    extras_require={
        'lint': [
            'mypy',
            'black',
            'isort',
        ],
        'test': [
            'pytest',
            'pytest-cov',
        ],
        'dist': [
            'build',
            'twine',
        ],
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
