from setuptools import setup, find_packages

with open('README.md', 'r') as file:
	long_description = file.read()

setup(
    name='qucircuit',
    version='2.0',
    license='GPL',
    author='Atul Varshneya',
    author_email='atul.varshneya@gmail.com',
	description='Quantum computer programming with circuits paradigm',
	long_description=long_description,
	long_description_content_type='text/markdown',
    packages=find_packages('.'),
    # package_dir={'': '.'},
    keywords='qsystems quantum computing',
	url='https://github.com/atulvarshneya/quantum-computing',
    install_requires=[
        'numpy',
        'qusimulator>=2.0'
        ]
    )
