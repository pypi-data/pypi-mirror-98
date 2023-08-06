import setuptools
from configparser import ConfigParser
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version(config_file='setup.cfg'):
    """
    Reads current version from configuration file
    """
    config = ConfigParser()
    config.read(config_file)
    return config['metadata']['version']

setuptools.setup(
    name="winregmgr",
    version=get_version(),
    author="Egor Wexler",
    author_email="egor.wexler@icloud.com",
    description="Context manager for Windows Registry manipulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuckyKarter/winregmgr",
    project_urls={
        "Bug Tracker": "https://github.com/LuckyKarter/winregmgr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",

)
