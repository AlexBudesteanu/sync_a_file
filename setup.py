#!/usr/bin/python3

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name='sync_files',
      author='Alexandru Budesteanu',
      author_email='alex.budesteanu@gmail.com',
      version='1.0',
      packages=['remote_file_sync'],
      py_modules=['syncfiles'],
      install_requires=[
          'click',
          'watchdog',
          'paramiko',
          'scp'
      ],
      entry_points={
          'console_scripts': ['syncfiles=syncfiles:main'],
      }
)