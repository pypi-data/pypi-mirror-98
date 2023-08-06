# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import navigation_icons

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='sphinx-navigation-icons',
    version=navigation_icons.__version__,
    url='https://github.com/dgarcia360/sphinx-navigation-icons',
    download_url='http://pypi.python.org/pypi/sphinx-navigation-icons',
    license='MIT',
    author='David Garcia',
    author_email='dgarcia360@outlook.com',
    description='Add image/font responsive icons to your Sphinx sidebar toctree',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    platforms='any',
    include_package_data=True,
    install_requires=['Sphinx>=2.0.0', 'beautifulsoup4'],
    packages=find_packages(exclude=['docs']),
    namespace_packages=['navigation_icons']
) 
