#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_namespace_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'tqdm', 'numpy', 'matplotlib'
               ,'networkx'
               ,'joblib'
               ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Danylo Lykov",
    author_email='lkvdan@gmail.com',
    python_requires='>=3.5',
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

    description="Utility to efficiently explore functions on their domains",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='cartesian_explorer',
    name='cartesian_explorer',
    packages=['cartesian_explorer.'+x for x in find_namespace_packages('cartesian_explorer')] + ['cartesian_explorer'], # This is horrible, how come there is no obvious simple solution for PEP-compliant packages?
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/danlkv/cartesian-explorer',
    version='0.1.13',
    zip_safe=False,
)
