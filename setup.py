import os
from setuptools import setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as f:
        return f.read()


setup(
    name="PySimpleGUI_Events",
    version="0.0.1",
    author="Jeffrey Yurkiw",
    author_email="jyurkiw@yahoo.com",
    description="A simple event handler system for PySimpleGUI",
    license="MIT",
    keywords="gui events",
    url="https://github.com/jyurkiw/PySimpleGUI_Events",
    packages=["PySimpleGUI_Events"],
    package_dir={'PySimpleGUI_Events': 'PySimpleGUI_Events'},
    long_description_content_type='text/markdown',
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
