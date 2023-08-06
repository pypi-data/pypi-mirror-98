"""
Setup module for install lib
"""
import os
from os import path
from typing import List

from setuptools import setup

MODULE_NAME = 'gen_doc'
LIB_NAME = 'gen_doc'
__version__ = '0.0.1'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_packages() -> List[str]:
    """
    Help method
    :return: List[str] path to files and folders library
    """
    ignore = ['__pycache__']

    list_sub_folders_with_paths = [x[0].replace(os.sep, '.')
                                   for x in os.walk(MODULE_NAME)
                                   if x[0].split(os.sep)[-1] not in ignore]
    return list_sub_folders_with_paths


setup(name=LIB_NAME,
      version=__version__,
      description='Module for build documentation',
      author='Denis Shchutkiy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='denisshchutskyi@gmail.com',
      url='https://github.com/Shchusia/gen_doc',
      packages=get_packages(),
      keywords=['pip', MODULE_NAME],
      entry_points={
          'console_scripts': [
              'gen_doc=gen_doc.commands:main'

          ]},
      )
