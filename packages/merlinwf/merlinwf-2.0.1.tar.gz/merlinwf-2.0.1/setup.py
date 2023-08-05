import os

from setuptools import find_packages, setup


version = "2.0.1"
DEPRECATION_MESSAGE = "The 'merlinwf' package has been deprecated and replaced by the 'merlin' package."


def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="merlinwf",
    author="Merlin Dev team",
    author_email="merlin@llnl.gov",
    version=version,
    description=DEPRECATION_MESSAGE,
    long_description=DEPRECATION_MESSAGE,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/LLNL/merlin",
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests"]),
    entry_points={
        "console_scripts": [
            "merlinwf=merlinwf.main:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
