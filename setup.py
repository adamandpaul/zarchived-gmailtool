"""setup.py script for gmailtool"""

from setuptools import setup, find_packages

setup(name='gmailtool',
      version='1.0.dev1',
      description='Command line tool for interacting with gmail',
      long_description = open('README.rst').read(),
      classifiers=[
          'Topic :: Communications :: Email', 
          'Programming Language :: Python',
      ],
      keywords='',
      author='Adam Terrey',
      author_email='software@adamandpaul.biz',
      url='https://github.com/adamandpaul/gmailtool',
      licence='gpl',
      packages=['gmailtool'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'python-dateutil',
          'google-api-python-client',
      ],
      entry_points="""
      [console_scripts]
      gmailtool = gmailtool.main:main
      """,
      )


