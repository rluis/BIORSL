from setuptools import setup

setup(
    name='BIORSL',
    version='0.0.6',
    packages=['bedEntry', 'bedContainer'],
    install_requires=['pysam==0.15.4'],
    url='https://github.com/rluis/BIORSL',
    license='GPL-3.0',
    author='rluis',
    author_email='ruisergioluis@gmail.com',
    description='A collection of python modules to computational biology analyses'
)
