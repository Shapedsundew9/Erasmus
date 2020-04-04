'''
Filename: /home/shapedsundew9/Projects/Erasmus/setup.py
Path: /home/shapedsundew9/Projects/Erasmus
Created Date: Wednesday, January 22nd 2020, 5:24:01 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='erasmus',
    version='0.0.1',
    description='Genetic programming',
    long_description=readme,
    author='Shapedsundew9',
    author_email='16618209+Shapedsundew9@users.noreply.github.com',
    url='https://github.com/Shapedsundew9/Erasmus',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True
)