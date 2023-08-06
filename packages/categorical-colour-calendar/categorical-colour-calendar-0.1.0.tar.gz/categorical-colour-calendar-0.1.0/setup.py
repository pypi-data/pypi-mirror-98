from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='categorical-colour-calendar',
    version='0.1.0',
    description='Library for drawing monthly calendars and highlighting dates from categorical data',
    packages=[''],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erichards97/categorical-colour-calendar',
    author='Edward Richards',
    author_email='',
    install_requires=[
        'pandas>=1.2.1',
        'matplotlib>=3.3.4'
    ],
    extras_require={
        'tests': [
            'pytest>=6.2.2',
        ],
        'dev': [
            'check-manifest>=0.46',
            'twine>=3.3.0',
            'wheel>=0.36.2',
            'pytest>=6.2.2',
            'tox>=3.23.0'
        ],
        'docs': [
            'sphinx==3.4.3'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)