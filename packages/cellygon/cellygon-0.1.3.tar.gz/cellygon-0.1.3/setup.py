#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

with open('requirements_dev.txt') as requirements_dev_file:
    setup_requirements = requirements_dev_file.read()
#setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Henrik Åhl",
    author_email='henrikaahl@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="create cellular meshes from segmented cells",
    entry_points={
        'console_scripts': [
            'cellygon=cellygon.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cellygon',
    name='cellygon',
    packages=find_packages(include=['cellygon', 'cellygon.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/supersubscript/cellygon',
    version='0.1.3',
    zip_safe=False,
)
