import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'mutable_primitives'
AUTHOR = 'Dr. Nick'
AUTHOR_EMAIL = 'das-intensity@users.noreply.github.com'
URL = 'https://github.com/das-intensity/mutable-primitives'

LICENSE = 'MIT Licence'
DESCRIPTION = 'Mutable classes of python primitives'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      py_modules=['mutable_primitives'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      )
