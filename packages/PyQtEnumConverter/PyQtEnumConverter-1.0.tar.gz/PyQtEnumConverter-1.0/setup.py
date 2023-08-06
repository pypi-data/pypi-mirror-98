#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8") as f:
    description = f.read()

setup(name='PyQtEnumConverter',
    version='1.0',
    description='Converts enums from PyQt5 to PyQt6',
    long_description=description,
    long_description_content_type='text/markdown',
    author='JakobDev',
    author_email='jakobdev@gmx.de',
    url='https://gitlab.com/JakobDev/PyQtEnumConverter',
    python_requires='>=3.7',
    include_package_data=True,
    install_requires=[
        'PyQt6',
    ],
     extras_require = {
        'Convert enums from QScintilla':  ['PyQt6-QScintilla']
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': ['PyQtEnumConverter = PyQtEnumConverter.PyQtEnumConverter:main']
    },
    license='GPL v3',
    keywords=['JakobDev','PyQt5','PyQt6','enum','update','port'],
    project_urls={
        'Issue tracker': 'https://gitlab.com/JakobDev/PyQtEnumConverter/-/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'Environment :: X11 Applications :: Qt',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Games/Entertainment',
        'Operating System :: OS Independent',
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
 )
