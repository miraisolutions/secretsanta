import os
import re
import glob
import sys
import shutil

from pathlib import Path
from setuptools import setup, find_packages, Command

PROJ_DIR = Path(__file__).parent.resolve()

PKG_NAME = 'secretsanta'

# distutils should not be depended on anymore, as it will be deprecated soon
DISTUTILS_LOG_LEVELS = {'WARN': 3, 'ERROR': 4}


def get_readme():
    with open(PROJ_DIR / 'README.md', encoding='utf-8') as fh:
        return fh.read()


def get_install_requirements():
    with open(PROJ_DIR / 'requirements-package.in', encoding='utf-8') as fh:
        return fh.readlines()


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(PROJ_DIR / PKG_NAME / '__init__.py', encoding='utf-8') as fh:
        return re.search('__version__ = [\'"]([^\'"]+)[\'"]', fh.read()).group(1)


class Publish(Command):
    command_name = 'publish'
    user_options = [
        ('wheel', None, 'Publish the wheel'),
        ('sdist', None, 'Publish the sdist tar'),
        ('no-clean', None, 'Don\'t clean the build artifacts'),
        ('sign', None, 'Sign the artifacts using GPG')
    ]
    boolean_options = ['wheel', 'sdist']

    def initialize_options(self):
        self.wheel = False
        self.sdist = False
        self.no_clean = False
        self.sign = False

    def finalize_options(self):
        if not (self.wheel or self.sdist):
            self.announce('Either --wheel and/or --sdist must be provided', DISTUTILS_LOG_LEVELS["ERROR"])
            sys.exit(1)

    def run(self):
        if os.system('pip freeze | grep twine'):
            self.announce('twine not installed.\nUse `pip install twine`.\nExiting.', DISTUTILS_LOG_LEVELS["WARN"])
            sys.exit(1)

        if self.sdist:
            os.system('python setup.py sdist')

        if self.wheel:
            os.system('python setup.py bdist_wheel')

        if self.sign:
            for p in glob.glob('dist/*'):
                os.system(f'gpg --detach-sign -a {p}')

        os.system('twine upload dist/*')
        # enter credentials for PyPI when prompted
        print('You probably want to also tag the version now:')
        print(f'  git tag -a {get_version()} -m \'version {get_version()}\'')
        print('  git push --tags')

        if not self.no_clean:
            shutil.rmtree('dist')
            shutil.rmtree('build')
            shutil.rmtree(PKG_NAME + '.egg-info')


# https://pypi.org/pypi?%3Aaction=list_classifiers
setup(
    name=PKG_NAME,
    version=get_version(),
    entry_points={
        'console_scripts': [
            'santa=secretsanta.cli.cli:santa',
        ],
    },
    description='Secret Santa randomizer',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
    ],
    keywords='secret santa',
    url='https://github.com/miraisolutions/secretsanta',
    author='Mirai Solutions',
    author_email='opensource@mirai-solutions.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*', 'tests.*.*')),
    install_requires=get_install_requirements(),
    zip_safe=False,
    cmdclass={
        'publish': Publish,
    },
)
