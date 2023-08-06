#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as req_file:
    requirements = req_file.readlines()

requirements = [
    "Click>=7.0",
    "numpy==1.18.1",
    "psims==0.1.30",
    "pymzml[plot]==2.4.6",
    "pyqms==0.6.2",
    "scipy",
    # "git+https://github.com/MKoesters/peptide_fragments.git@feature/add_fragment_method",
    "peptide_fragments @ git+ssh://git@github.com/MKoesters/peptide_fragments@feature/add_fragment_method#egg=peptide_fragments",
    "loguru==0.4.1",
    "intervaltree==3.1.0",
    "pyteomics==4.3.3",
    "tqdm==4.59.0",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Manuel Kösters",
    author_email="manuel.koesters@dcb.unibe.ch",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Library to create synthetic mzMLs file based on chemical formulas",
    entry_points={
        "console_scripts": [
            "smiter=smiter.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords="smiter",
    name="smiter",
    packages=find_packages(include=["smiter", "smiter.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/MKoesters/smiter",
    version="0.1.0",
    zip_safe=False,
)
