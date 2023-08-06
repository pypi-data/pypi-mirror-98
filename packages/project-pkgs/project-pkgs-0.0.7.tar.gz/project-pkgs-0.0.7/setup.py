'''
Date: 2020-12-22 11:29:49
LastEditors: Rustle Karl
LastEditTime: 2021-03-12 12:22:59
'''
import os.path

from setuptools import setup

# What packages are required for this module to be executed?
requires = [

]

# Import the README and use it as the long-description.
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='project-pkgs',
    py_modules=['color', 'checksum'],
    packages=['logger'],
    version='0.0.7',
    license='BSD',
    author='Rustle Karl',
    author_email='fu.jiawei@outlook.com',
    description='个人项目常用库',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['color', 'logger', 'pkgs'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=requires,
)
