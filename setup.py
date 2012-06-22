from setuptools import setup, find_packages

setup(
    name='espresso',
    description='A tool to easily manage small configurations',
    version='0.2',
    author='Jorge E. Cardona',
    author_email='jorgeecardona@gmail.com',
    packages=find_packages(),
    license="BSD",
    test_suite='tests',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        ],
    entry_points={
        'console_scripts': [
            'barista = espresso.cli:barista',
            ],
        },
    install_requires=[
        'pbs==0.105',
        'PyYAML==3.10'],
    setup_requires=[
        'mock']
    )
