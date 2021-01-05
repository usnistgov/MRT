# PURPOSE

The purpose of this software is to offer a graphical user interface (GUI) for performing modified rhyme test (MRT) intelligibility research. MRT intelligibility is a subjective measure of how intelligible a given keyword is. Subjects are played audio and asked to select the keyword they think they have heard from a list of 6 keywords. The keywords are all structured as consonant-vowel-consonant. Each list contains keywords that rhyme in a certain sense: either the leading or trailing consonant varies between words in a batch.

# Building and Installing the Package Locally

To build the package
```#remove old packages and stuff
 rm -r dist
 rm -r build

 #pull the latest version
 git pull

 # run setup script
 py setup.py sdist bdist_wheel
 ```

 To install the package

 ```
 #remove the old package
 python -m pip uninstall mrt-nist

 # install the new package
 python -m pip install --find-links ./dist/ mrt-nist
 ```

# RUNNING MRT SOFTWARE

To run the test software run MRT.py. You must have a compatible test directory containing test audio and session playlists. More information on these requirements to come in the future...

# DISCLAIMER

This software was developed by employees of the National Institute of Standards and Technology (NIST), an agency of the Federal Government. Pursuant to title 17 United States Code Section 105, works of NIST employees are not subject to copyright protection in the United States and are considered to be in the public domain. Permission to freely use, copy, modify, and distribute this software and its documentation without fee is hereby granted, provided that this notice and disclaimer of warranty appears in all copies.

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT SHALL NIST BE LIABLE FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY CONNECTED WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.
