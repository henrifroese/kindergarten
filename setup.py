#!/usr/bin/env python

from setuptools import setup, find_packages

version = "0.0.5"

requirements = [
    "dash-bootstrap-components>=1.2.0",
    "dash>=2.6.0",
    "pandas>=1.3.5",
    "plotly>=5.9.0",
    "jupyter-dash>=0.4.2",
]

test_requirements = ["pip", "bump2version", "wheel", "watchdog", "black", "pytest"]

setup(
    author="Henri Froese",
    author_email="henri.froese@yahoo.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Kindergarten is a UI on top of Plotly to easily visualize Pandas DataFrames.",
    install_requires=requirements,
    license="MIT license",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="kindergarten",
    name="kindergarten",
    packages=find_packages(include=["kindergarten", "kindergarten.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/henrifroese/kindergarten",
    version=version,
    zip_safe=False,
)
