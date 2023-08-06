#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup python package."""

from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements:
    requirements = requirements.readlines()

EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(
    author_email="rafaelagd@gmail.com",
    author="Rafael Garcia-Dias",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A tool to perform Freesurfer volume Harminization in unseen scanner.",
    entry_points={"console_scripts": ["mriqc-run=neuroharmony.models.mriqc:main"]},
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    install_requires=requirements,
    keywords="Harminization, MRI, data science",
    license="MIT license",
    long_description=readme,
    name="Neuroharmony",
    package_dir={"neuroharmony": "neuroharmony",
                 "models": "neuroharmony.models",
                 "neuroCombat": "neuroharmony.models.neuroCombat",
                 },
    packages=find_packages(),
    python_requires='>=3.6',
    test_suite="pytest",
    url="https://github.com/garciadias/Neuroharmony",
    version="0.1.7",
    zip_safe=False,
)
