# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from testbrain import __version__


setup(
    name='testbrain',

    version=__version__,
    license='unlicensed',

    description='Command Line Interface for Appsurify Testbrain.',
    long_description='Command Line Interface for Appsurify Testbrain.',
    long_description_content_type='text/markdown',

    keywords='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    project_urls={},
    url='https://github.com/invertednz/Appsurify',
    author='Artem Demidenko',
    author_email='ar.demidenko@gmail.com',

    packages=find_packages(),
    # packages=['testbrain', ],
    # package_dir={},
    package_data={'testbrain': ['templates/*.py-tpl']},

    include_package_data=True,

    python_requires='>=2.7,<2.8',
    install_requires=[
        'requests',
        'Click',
        'configparser',
        'shutils',
        'pymysql==0.10.1'

    ],
    extras_require={},
    scripts=['bin/tb'],
    entry_points={
        'console_scripts': [
            'testbrain=testbrain.__main__:cli',
        ],
    },
)
