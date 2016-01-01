from setuptools import setup, find_packages

setup(
    name='seamus',
    version='0.0.1',
    author='Ankit Chandawala',
    author_email='ankitchandawala@gmail.com',
    url='https://github.com/nerandell/seamus',
    description='Makes testing refactored code easy',
    packages=find_packages(exclude=['tests']),
)
