from setuptools import setup, find_packages

with open('README.md', 'r') as file:
	long_description = file.read()

setup(
    name='qusimulator',
    version='1.5.1',
    license='GPL',
    author='Atul Varshneya',
    author_email='atul.varshneya@gmail.com',
	description='Quantum computer simulator',
	long_description=long_description,
	long_description_content_type='text/markdown',
    packages=find_packages('.'),
    # package_dir={'': '.'},
    keywords='qsystems quantum computing',
	url='https://github.com/atulvarshneya/quantum-computing',
    install_requires=[
        'numpy'
        ],
    # scripts=['qcli.py']
	entry_points = {
		'console_scripts': ['qsimcli=qsim.qcli:main'],
	}
    )
