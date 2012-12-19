from setuptools import setup, find_packages

# Requires.
install_requires = ['configparser>=3.2', 'argparse', 'distribute', 'fstab', 'sh']

try:
    import importlib
except ImportError:
    install_requires.append('importlib')


setup(
    name='espresso',
    description='Manage the configuration of your servers easily.',
    version='1.0.19',
    url='http://github.com/jorgeecardona/espresso',
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
    install_requires=install_requires,
    setup_requires=['distribute']
    )
