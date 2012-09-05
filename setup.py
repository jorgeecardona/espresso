from setuptools import setup, find_packages

setup(
    name='espresso',
    description='Manage your servers easily',
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
			'espresso = espresso.daemon:espresso',
            ],
        },
    install_requires=['pyzmq>=2.2.0.1', 'gevent'],
    setup_requires=[
        'mock']
    )
