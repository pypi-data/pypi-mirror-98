import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The full path to the README file
README_FILE = os.path.join(HERE, "README.md")

with open(README_FILE) as f:
	README = f.read()

# This call to setup() does all the work
setup(
    name="linkedtuple",
    version="1.0.0",
    packages=["linkedtuple"],

    description="A LinkedTuple is a read-only structure of linked (nested) tuples much like lists in functional languages",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Gato-X/python-LinkedTuple",
    author="Guillermo Romero (Gato-X)",
    author_email="gato@felingeneering.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=[],
)
