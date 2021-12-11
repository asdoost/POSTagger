import os
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="POSTagger",
    version="v0.1.13-beta",
    description="A GUI app for semi-automatic POS tagging",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords = "POS Tagger, Part of Speech Tagger",
    url="https://github.com/asdoost/POSTagger",
    download_url = "https://github.com/asdoost/POSTagger/archive/refs/tags/v0.1.13-beta.tar.gz",
    author="Abbas Safardoost",
    author_email="a.safardoust@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6"
    ],
    packages=["POSTagger"],
    package_dir={"POSTagger": "POSTagger"},
    package_data={
        "POSTagger": [
            "corpora/*.txt", 
            "imgs/*.png",
            "outputs/*",
            "projects/*.proj",
            "tagsets/*.csv"]
    },
    entry_points={
        "console_scripts": [
            "POSTagger=POSTagger.POSTagger:POSTagger",
        ]
    },
    install_requires=[
        "arabic_reshaper",
        "python-bidi"
        ]
)
