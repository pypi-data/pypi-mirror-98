# -*- coding: utf-8 -*-


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='datasets-bleu',
    version='0.2',
    description='',
    long_description=long_description,
    author='Spider',
    author_email='18128872727@163.com',
    url='https://github.com/',
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['tenacity', 'Faker'],
    packages=setuptools.find_packages(),
)
