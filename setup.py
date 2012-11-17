from setuptools import setup, find_packages

setup(
    name='espresso',
    description='Manage the configuration of your servers easily.',
    version='1.0.13',
    author='Jorge E. Cardona',
    author_email='jorge@cardona.co',
    packages=['espresso'],
    license="BSD",
    test_suite='tests',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        ],
    entry_points={
        'console_scripts': [
            'setup-espresso = espresso.cli:setup',
            'espresso = espresso.cli:main'
            ],
        },
    install_requires=[
        'configparser>=3.2', 
        'distribute',
        'fstab',
        'sh'],
    setup_requires=['distribute']
    )
