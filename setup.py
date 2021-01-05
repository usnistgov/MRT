# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mrt-nist", # Replace with your own username
    version="0.0.1",
    author="Jaden Pieper",
    author_email="jaden.pieper@nist.gov",
    description="Modified Rhyme Test Speech Intelligibility Graphical User Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usnistgov/mrt",
    packages=setuptools.find_packages(),
    use_scm_version={'write_to' : 'mrt/version.py'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'tkinter',
        'numpy',
        'scipy',
        'sounddevice',
    ],
    python_requires='>=3.6',
)