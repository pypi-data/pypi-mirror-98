from setuptools import setup, find_packages
from pacemaker import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pacemaker",
    version=__version__,
    author="Keshav Murthy",
    author_email="mkeshav@gmail.com",
    description="To keep the old heart ticking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkeshav/pace-maker.git",
    packages=find_packages(include=('pacemaker',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)