import pathlib
from setuptools import setup
from youtube import Config

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="youtube.py",
    version=Config.__version__,
    description="YouTube.py is a light python module for youtube.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://youtube-python.mayankfawkes.xyz/",
    author="Mayank Gupta",
    author_email="mayankfawkes@gmail.com",
    license="MIT License",
    project_urls={
            "Documentation": "https://youtube-python.readthedocs.io",
            "Source": "https://github.com/youtube-py/youtube.py",
        },
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        'Topic :: System :: Networking',
        'Topic :: Internet :: WWW/HTTP',
        "Topic :: Multimedia :: Video",
        "Natural Language :: English",
        'Environment :: Plugins',
        "Environment :: Console",
        "Topic :: Terminals",
        "Topic :: Utilities",
        ],
    entry_points={
        "console_scripts": ["youtube = youtube.Cli:main"],
        },
    packages=["youtube"],
    python_requires=">=3.6",
    keywords=["Youtube", "youtube.py", "Youtube Python", "Python Youtube", "Youtube downloader", "Youtube Videos"],
    include_package_data=True,
    install_requires=["requests"],
)
