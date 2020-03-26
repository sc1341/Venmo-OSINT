
from setuptools import setup, find_packages

setup(
    name='Venmo OSINT',
    version='1.0',
    description='Scrapes a user\'s Venmo account for payment history',
    author='sc1341',
    author_email='',
    packages=find_packages(),
    url='https://github.com/sc1341/Venmo-OSINT',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'argparse',
    ],
    entry_points='''
        [console_scripts]
        venmo-osint=venmoosint:main
    ''',
    keywords='venmo scrape osint OSINT Venmo money banking information gathering',
)
