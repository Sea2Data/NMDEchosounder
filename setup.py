from setuptools import setup
from os.path import join as pjoin
from setuptools import setup, find_packages
import versioneer



# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
INSTALL_REQUIRES = [t.strip() for t in requirements]


setup(name='runLSSSreport',
      version='1.0',
      description='This package provides functionality for downloading, reading and writing xml-formats defined by NMD in PYTHON.',
      url='https://github.com/sindrevatnehol/sonarNetCDFconverter/',
      author='Sindre Vatnehol',
      author_email='sindre.vatnehol@hi.no',
      license='GPL3',
      install_requires=INSTALL_REQUIRES,
      packages=['runLSSSreport',],
      zip_safe=False)

