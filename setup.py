import re
import os.path as op


from codecs import open
from setuptools import setup, find_packages


def read(fname):
    ''' Return the file content. '''
    here = op.abspath(op.dirname(__file__))
    with open(op.join(here, fname), 'r', 'utf-8') as fd:
        return fd.read()


readme = read('README.md')
changelog = read('docs/CHANGELOG.rst').replace('.. _changelog:', '')

install_requirements = [
    "requests>=2.26.0",
    "requests_mock>=1.9.3",
    "zeep>=4.1.0",
    "dicttoxml>=1.7.4",
    "PyYAML>=6.0",
    "jinja2>=3.0.3",
]

version = ''
version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    read(op.join('cdiscountapi', '__init__.py')),
                    re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(
    name='cdiscountapi',
    author='Taurus Olson',
    author_email='taurusolson@gmail.com',
    version=version,
    description='A Python API for Cdiscount marketplace',
    long_description=readme + '\n\n' + changelog,
    keywords=['api', 'cdiscount', 'python'],
    packages=find_packages(),
    install_requires=install_requirements,
    zip_safe=True,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
