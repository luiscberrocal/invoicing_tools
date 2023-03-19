#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Luis Carlos Berrocal",
    author_email='luis.berrocal.1942@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tool to generate invoices.",
    entry_points={
        'console_scripts': [
            'invoicing_tools=invoicing_tools.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='invoicing_tools',
    name='invoicing_tools',
    packages=find_packages(include=['invoicing_tools', 'invoicing_tools.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luiscberrocal/invoicing_tools',
    version='0.3.3',
    zip_safe=False,
)
