
from setuptools import setup, find_packages
from pathlib import Path
import sys

VERSION = (Path(__file__).parent / 'clss' / 'VERSION').open('r').read().strip()

setup(
  name='clss',
  description='Command-line utility for syncing with Google Sheets',
  version=VERSION,
  long_description_content_type='text/markdown',
  long_description=open('README.md', 'r').read(),

  url='https://gitlab.com/franksh/clss/',
  author='Frank S. Hestvik',
  author_email='tristesse@gmail.com',
  
  license='MIT',
  keywords='google-api spreadsheets sheets google api'.split(),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Environment :: Console",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],

  packages=find_packages(),
  install_requires=[
    'google-api-python-client==2.*',
    'google-auth-httplib2==0.1.*',
    'google-auth-oauthlib==0.4.*',
    'click',
  ],
  python_requires='>=3.7',
  zip_safe=False,
  entry_points={
    'console_scripts': ['clss = clss.cli:main'],
  },
  package_data={
    "clss": [
      "VERSION",
    ],
  },
  include_package_data=True,
)

