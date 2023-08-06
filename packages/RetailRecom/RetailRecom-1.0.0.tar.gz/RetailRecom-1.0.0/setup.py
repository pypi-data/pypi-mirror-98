from setuptools import setup

setup(name='RetailRecom',
      version='1.0.0',
      description='Simple Recommendation System in Python3+ (Using Collaborative Filtering)',
      author='Shashimal Senarath',
      packages=['src'],
      license="MIT",
      keywords="Recommendation Retail",
      install_requires=['pyspark', 'elasticsearch', 'os']
      )