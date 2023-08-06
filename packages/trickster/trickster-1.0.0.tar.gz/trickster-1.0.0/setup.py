"""Install Double and dependencies."""

import sys

from setuptools import setup


def main():
    setup(
        name='trickster',
        version='1.0.0',
        python_requires='>=3.6',
        description='Mocking Service',
        long_description='',
        url='https://github.com/JakubTesarek/trickster',
        author='Jakub Tesárek',
        author_email='jakub@tesarek.me',
        license='unlicensed',
        include_package_data=True,
        packages=['trickster'],
        install_requires=[
            'flask',
            'fastjsonschema',
            'basicauth'
        ],
        extras_require={
            'dev': [
                'setuptools',
                'wheel',
                'flake8',
                'flake8-docstrings',
                'flake8-pytest',
                'flake8-eradicate',
                'flake8-print',
                'flake8-todo',
                'pytest',
                'pytest-repeat',
                'pytest-cov',
                'pytest-mock',
                'mypy',
                'twine'
            ]
        }
    )


if __name__ == '__main__':
    main()