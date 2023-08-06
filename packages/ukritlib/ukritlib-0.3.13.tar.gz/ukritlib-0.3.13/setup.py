import os
import os.path
from setuptools import setup,find_packages

## Function ในการดึงข้อมูล README.md มาแสดง ในหน้า pypi
def readme():
    with open('README.md') as f:
        return f.read()

# TODO ######################################################## SETTING
## ชื่อ Packeage ที่ เราต้องการ
NAME='ukritlib'

## Packeage Version ที่ เราต้องการ
VERSION='0.3.13'

## https://pypi.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Science/Research",
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Software Development :: Libraries"
]

MAINTAINER = "UkritFB"
MAINTAINER_EMAIL = "ukrit.fb@gmail.com"
DESCRIPTION = "Testing Python Package From Ukrit Fongsomboon"
KEYWORDS = "python medical imaging"
URL = "https://github.com/ukritfongsomboon/ukritlib"
DOWNLOAD_URL = "https://github.com/pydicom/pydicom/archive/master.zip"




# TODO ########################################################

setup(name=NAME,  
      version=VERSION,
      classifiers=CLASSIFIERS,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      long_description=readme(),  ## ใช้สำหรับการโชว์ข้อมูล
      long_description_content_type="text/markdown",  ## บอกว่าในการใช้งาน Description ใช้งาน README.md

      test_suite='nose.collector',
      tests_require=['nose'],

      keywords=KEYWORDS,
      description=DESCRIPTION,

      url=URL,
      download_url=DOWNLOAD_URL,
      
      author='Ukrit Fongsomboon',
      author_email='ukrit.fb@gmail.com',

      license='MIT',

    #   packages=['ukritlib'],
      packages = find_packages(),
      include_package_data = True,

      zip_safe=False)
