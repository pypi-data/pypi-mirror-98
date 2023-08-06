"""https://packaging.python.org/en/latest/distributing.html"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='provenance_tools',
    version='0.0.2',
    description='provenance_tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/acil-bwh/provenance_tools',
    author='James Ross',
    author_email='jross@bwh.harvard.edu',

    scripts=[
        'bin/provenance_initializer'],
    
    ### Other stuff ...
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'provenance_tools=provenance_tools.write_provenance_data:write_provenance_data',
            ],
    },
)
