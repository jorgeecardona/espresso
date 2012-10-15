from setuptools import setup, find_packages

setup(
    name='espresso',
    description='Manage the configuration of your servers easily.',
    version='0.3',
    author='Jorge E. Cardona',
    author_email='jorge@cardona.co',
    packages=find_packages(),
    license="BSD",
    test_suite='tests',
    namespace_packages=['espresso.plugins'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        ],
    entry_points={
        'console_scripts': [
			'espresso = espresso.daemon:espresso',
            ],
        'espresso.plugins': [
            'supervisor = espresso.plugins.supervisor:supervisor'
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
