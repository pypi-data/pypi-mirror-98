import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rickle",
    version="0.0.0",
    description="A stack-based concatenative programming language",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Takk",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[]
)