import io
import os
import re

from setuptools import setup, find_packages

PROJ_DIR = os.path.abspath(os.path.dirname(__file__))
# PROJ_DIR = os.getcwd()


def get_readme():
    with io.open(os.path.join(PROJ_DIR, 'README.md'), encoding='utf-8') as fh:
        return fh.read()


def get_install_requirements():
    with io.open(os.path.join(PROJ_DIR, 'requirements-package.in'), encoding='utf-8') as fh:
        return fh.readlines()


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with io.open(os.path.join(PROJ_DIR, 'secretsanta', '__init__.py'), encoding='utf-8') as fh:
        return re.search('__version__ = [\'"]([^\'"]+)[\'"]', fh.read()).group(1)


# https://pypi.org/pypi?%3Aaction=list_classifiers
setup(
    name='secretsanta',
    version=get_version(),
    description='Secret Santa randomizer',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
    ],
    keywords='secret santa',
    url='https://github.com/miraisolutions/secretsanta',
    author='RSc',
    author_email='roland.schmid@mirai-solutions.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*', 'tests.*.*')),
    install_requires=get_install_requirements(),
    zip_safe=False
)
