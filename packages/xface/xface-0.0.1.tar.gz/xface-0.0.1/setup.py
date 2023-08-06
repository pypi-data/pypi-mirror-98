
#! /usr/bin/env python
# encoding: utf-8

# Always prefer setuptools over distutils
from setuptools import setup


pypi_name = 'xface'


setup(
    name=pypi_name,
    version='0.0.1',
    keywords=pypi_name,
    description=pypi_name,
    long_description=pypi_name,
    url='https://github.com/007gzs/%s' % pypi_name,
    author='007gzs',
    author_email='007gzs@sina.com',
    license='LGPL v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[],
    install_requires=[],
    zip_safe=False,
    include_package_data=True
)
