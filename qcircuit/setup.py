from setuptools import setup, find_packages

with open('README.md', 'r') as file:
	long_description = file.read()

setup(
    name='qcircuit',
    version='1.5',
    license='GPL',
    author='Atul Varshneya',
    author_email='atul.varshneya@gmail.com',
	description='Quantum computer programming with circuits paradigm',
	long_description=long_description,
	long_description_content_type='text/markdown',
    packages=find_packages('.'),
    # package_dir={'': '.'},
    keywords='qsystems quantum computing',
    install_requires=[
        'numpy',
        'qsimulator>=1.5'
        ]
    )
