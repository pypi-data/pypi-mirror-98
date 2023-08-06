import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="exploratium-quant",  # Replace with your own username
    version="0.0.3",
    author="Carlos Rivera",
    author_email="carlos@synx.ai",
    description="ETL library to download and pre-process financial data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/exploratium/quant-cli",
    project_urls={
        "Bug Tracker": "https://github.com/exploratium/quant-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=setuptools.find_packages(where="./"),
    python_requires=">=3.6",
    py_modules=['exploratium', 'utils'],
    install_requires=[
        'click',
        'blessed',
        'pandas-datareader'
    ],
    scripts=['bin/quant-cli'],
)
