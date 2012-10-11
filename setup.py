from setuptools import setup, find_packages

setup(
    name='espresso',
    description='Manage the configuration of your servers easily.',
    version='0.2',
    author='Jorge E. Cardona',
    author_email='jorge@cardona.co',
    packages=find_packages(),
    license="BSD",
    test_suite='tests',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        ],
    entry_points={
        'console_scripts': [
			'espresso = espresso.daemon:espresso',
            ],
        },
    install_requires=[
        'distribute',
        'sh'],
    setup_requires=[
        'distribute',
        'mock']
    )
