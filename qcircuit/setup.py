from setuptools import setup, find_packages

setup(
    name='qckt',
    version='1.1',
    license='GPL',
    author='Atul Varshneya',
    author_email='atul.varshneya@gmail.com',
    # packages=find_packages('.'),
    package_dir={'': '.'},
    keywords='qsystems quantum computing',
    install_requires=[
        'numpy',
        'qsim'
        ]
    )
