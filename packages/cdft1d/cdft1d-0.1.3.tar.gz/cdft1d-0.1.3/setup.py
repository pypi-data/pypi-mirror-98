from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cdft1d',
    version='0.1.3',
    url='',
    license='',
    author='Marat Valiev and Gennady Chuev',
    author_email='marat.valiev@gmail.com',
    description='Classical density functional theory code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['cdft1d', 'cdft1d.*']),
    include_package_data=True,
    package_data={'': ['data/*']},
    install_requires=[
            'scipy>=1.6.1',
            'numpy>=1.20.1',
            'matplotlib>=3.3.4',
            'click'
    ],
    entry_points={
        'console_scripts': [
            'rism = cdft1d.cli:rism'
        ]
    }
)
