from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in utm_shortener/__init__.py
from utm_shortener import __version__ as version

setup(
    name="utm_shortener",
    version=version,
    description="UTM Parameter Generation and URL Shortening for Frappe",
    author="Chinmay Bhatk",
    author_email="chinmay@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)