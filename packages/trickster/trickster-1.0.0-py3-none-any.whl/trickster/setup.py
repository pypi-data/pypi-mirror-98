"""Install lmc-radlib and dependencies."""

import sys

from setuptools import setup


def main():
    setup(
        name='double',
        version='1.0.0',
        python_requires='>=3.6',
        description='Mocking Service',
        long_description='',
        url='https://github.com/JakubTesarek/double',
        author='Jakub Tesárek',
        author_email='jakub@tesarek.me',
        license='unlicensed',
        include_package_data=True,
        packages=['double'],
        install_requires=[
            'python-rapidjson'
        ],
        extras_require={
            'dev': [
                'setuptools',
                'wheel',
                'pytest',
                'pytest-cov',
                'pytest-mock',
                'mypy',
                'flake8',
                'flake8-colors',
                'flake8-eradicate',
                'flake8-print',
                'flake8-todo',
                'confluent-kafka',
                'kafka-python',
                'twine'
            ],
            'kafka': [
                'confluent-kafka'
            ]
        }
    )


if __name__ == '__main__':
    main()