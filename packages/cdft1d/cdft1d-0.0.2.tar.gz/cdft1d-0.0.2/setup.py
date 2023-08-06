from setuptools import setup, find_packages

setup(
    name='cdft1d',
    version='0.0.2',
    url='',
    license='',
    author='Marat Valiev and Gennady Chuev',
    author_email='marat.valiev@gmail.com',
    description='Classical density functinal theiory code',
    packages=find_packages(include=['cdft1d', 'cdft1d.*']),
    include_package_data=True,
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
