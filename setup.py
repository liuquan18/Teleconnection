from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'sphinx',
    ],
)
