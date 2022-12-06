import finddata
from setuptools import setup, find_packages

setup(
    name="brabbl",
    author="Jonas und der Wolf GmbH",
    author_email="info@jonasundderwolf.de",
    version="2.0.1b0",
    packages=find_packages(),
    package_data=finddata.find_package_data(),
    include_package_data=True,
)
