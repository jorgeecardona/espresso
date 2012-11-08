from setuptools import setup, find_packages

setup(
    name='espresso',
    description='Manage the configuration of your servers easily.',
    version='1.0',
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
            'setup-espresso = espresso.setup:main',
            'espresso = espresso.espresso:main'
            ],
        },
    install_requires=[
        'distribute',
        'sh',
        'gevent'],
    setup_requires=[
        'distribute',
        'mock']
    )
