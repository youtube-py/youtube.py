import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="youtube.py",
    version="1.0.0",
    description="YouTube.py is a light python module for youtube.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/youtube-py/youtube.py",
    author="Mayank Gupta",
    author_email="mayankfawkes@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["youtube"],
    include_package_data=True,
    install_requires=[],
)
