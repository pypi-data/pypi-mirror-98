#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# try:
#   python3 -m pip --version
# except:
#   try:
#       python3 -m ensurepip --default-pip
#   except:
#       wget https://bootstrap.pypa.io/get-pip.py
#       python3 get-pip.py
# finally:
#   python3 -m pip install --upgrade pip setuptools wheel

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

# python3 -m venv tutorial_env
# source tutorial_env/bin/activate
# rm -rf build
# rm -rf src/*.egg-info
# python3 setup.py sdist
# tox -e check
# python3 setup.py clean --all sdist bdist_wheel
# twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip

# rm -rf dist build */*.egg-info *.egg-info
# python3 setup.py sdist
# 

# import os
# import sys
# from shutil import rmtree

# from setuptools import Command, find_packages, setup

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='LRphase',
    version='0.3.1',
    license='MIT',
    description='Phasing individual long reads using known haplotype information.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    #author='Ion\\"\'el Cristian M\\u0103rie\\u0219',
    author='Greg Farnum',
    author_email='gregfar@umich.edu',
    url='https://github.com/LRphase/LRphase_CLI',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control :: Git'
        # 'Development Status :: 5 - Production/Stable',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        # 'Operating System :: Unix',
        # 'Operating System :: POSIX',
        # 'Operating System :: Microsoft :: Windows',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # # uncomment if you test on these interpreters:
        # # 'Programming Language :: Python :: Implementation :: IronPython',
        # # 'Programming Language :: Python :: Implementation :: Jython',
        # # 'Programming Language :: Python :: Implementation :: Stackless',
        # 'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/LRphase/LRphase_CLI/issues',
    },
    keywords=[
              'long-reads', 'phasing', 'haplotype',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    install_requires=[
        'pysam>=0.15.4', 'biopython>=1.78', 'pyliftover>=0.4', 'setuptools',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'LRphase = LRphase.cli:main',
        ]
    },
)



# with open('README.md', 'r') as fh:
    # long_description = fh.read()

# with open('requirements.txt', 'r') as requirements_file:
     # requirements_text = requirements_file.read()
# requirements = requirements_text.split()

# # Package meta-data.
# NAME = 'LRphase'
# DESCRIPTION = 'Phasing individual long reads using known haplotype information.'
# URL = 'https://github.com/LRphase/LRphase_CLI'
# EMAIL = 'gregfar@umich.edu, mhholmes@umich.edu'
# AUTHOR = 'Greg Farnum, Monica Holmes'
# REQUIRES_PYTHON = '>=3.6'
# VERSION = '0.2.1.2'
# LICENSE = 'MIT'
#REQUIRED = requirements
#here = os.path.abspath(os.path.dirname(__file__))

#about = {}
# if not VERSION:
    # with open(os.path.join(here, NAME, '__version__.py')) as f:
        # exec(f.read(), about)
# else:
    # about['__version__'] = VERSION

# setup(
        # name = NAME,
        # version = VERSION, #about['__version__'],
        # description = DESCRIPTION,
        # long_description_content_type = 'text/markdown',
        # long_description = long_description,
        # author = AUTHOR,
        # author_email = EMAIL,
        # python_requires = REQUIRES_PYTHON,
        # url = URL,
        # setup_requires = 
        # [
        # 'pysam', 
        # 'pyliftover', 
        # 'biopython', 
        # 'setuptools',
        # 'importlib',
        # 'requests'
        # ],
        # #'importlib',
        # #'requests',
        # #setup_requires = requirements,
        # #install_requires = requirements,
        # #include_package_data = True,
        # packages=find_packages('LRphase'),
        # package_dir={'': 'src'},
        # #package_dir={':','LRphase'},
        # #package_data=
        # #{
        # #'': ['data/*'],
        # #},
        # py_modules = ['LRphase','InputData','SimulatePhasedData','PhasableSample','PhasedRead','PhaseSet','HeterozygousSites','urls'],
        # #py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
        # entry_points={'console_scripts': ['LRphase = LRphase:main']},
        # license = LICENSE,
        # classifiers = [
                # # Trove classifiers
                # # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
                # 'License :: OSI Approved :: MIT License',
                # 'Programming Language :: Python',
                # 'Programming Language :: Python :: 3',
                # 'Programming Language :: Python :: 3.6',
                # 'Programming Language :: Python :: 3.7',
                # 'Programming Language :: Python :: 3.8',
                # 'Programming Language :: Python :: 3.9',
                # 'Programming Language :: Python :: Implementation :: CPython',
                # 'Programming Language :: Python :: Implementation :: PyPy',
                # 'Intended Audience :: Science/Research',
                # 'Natural Language :: English',
                # 'Operating System :: Microsoft',
                # 'Operating System :: MacOS',
                # 'Operating System :: Unix',
                # 'Programming Language :: Python',
                # 'Topic :: Documentation',
                # 'Topic :: Scientific/Engineering :: Bio-Informatics',
                # 'Topic :: Software Development :: Libraries :: Python Modules',
                # 'Topic :: Software Development :: Version Control :: Git'
                
                # ],
        # )
        
        
#
        # # $ setup.py publish support.
        # cmdclass = {
                # 'upload':UploadCommand,
                # },
        # )
        # #namespace_packages = NAMESPACES,
        # #packages = PACKAGES,
        # #py_modules = PY_MODULES,
        # #entry_points = {
                # #'console_scripts':['LRphase=LRphase:main'],
                # #},
        # install_requires = REQUIRED,
        # include_package_data = True,
        # packages=find_packages('src'),
        # package_dir={'': 'src'},
        # package_data=
        # {
        # '': ['data/error_tables/*'],
        # },
        # py_modules = ['LRphase','InputData','SimulatePhasedData','PhasableSample','PhasedRead','PhaseSet','HeterozygousSites'],
        # entry_points={'console_scripts': ['LRphase = LRphase:main']},
        # license = LICENSE,
        # classifiers = [
                # # Trove classifiers
                # # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
                # 'License :: OSI Approved :: MIT License',
                # 'Programming Language :: Python',
                # 'Programming Language :: Python :: 3',
                # 'Programming Language :: Python :: 3.6',
                # 'Programming Language :: Python :: 3.7',
                # 'Programming Language :: Python :: 3.8',
                # 'Programming Language :: Python :: 3.9',
                # 'Programming Language :: Python :: Implementation :: CPython',
                # 'Programming Language :: Python :: Implementation :: PyPy',
                # 'Intended Audience :: Science/Research',
                # 'Natural Language :: English',
                # 'Operating System :: Microsoft',
                # 'Operating System :: MacOS',
                # 'Operating System :: Unix',
                # 'Programming Language :: Python',
                # 'Topic :: Documentation',
                # 'Topic :: Scientific/Engineering :: Bio-Informatics',
                # 'Topic :: Software Development :: Libraries :: Python Modules',
                # 'Topic :: Software Development :: Version Control :: Git'
                
                # ],
        # )
        # # $ setup.py publish support.
        # # cmdclass = {
                # # 'upload':UploadCommand,
                # # },
        # # )
# # NAMESPACES = [f"LRphase"]
# # PY_MODULES = ['urls']
# # PACKAGES = find_packages()#include=['InputData','PhasedRead','PhaseSet','HeterozygousSites','PhasableSample','urls']),

# here = os.path.abspath(os.path.dirname(__file__))

# about = {}
# if not VERSION:
    # with open(os.path.join(here, NAME, '__version__.py')) as f:
        # exec(f.read(), about)
# else:
    # about['__version__'] = VERSION


# class UploadCommand(Command):
    # """Support setup.py upload."""

    # description = 'Build and publish the package.'
    # user_options = []

    # @staticmethod
    # def status(s):
        # """Prints things in bold."""
        # print('\033[1m{0}\033[0m'.format(s))

    # def initialize_options(self):
        # pass

    # def finalize_options(self) -> object:
        # pass

    # def run(self):
        # try:
            # self.status('Removing previous builds…')
            # rmtree(os.path.join(here, 'dist'))
        # except OSError:
            # pass

        # self.status('Building Source and Wheel (universal) distribution…')
        # os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        # self.status('Uploading the package to PyPi via Twine…')
        # os.system('twine upload dist/*')

        # self.status('Pushing git tags…')
        # os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        # sys.exit()

    # def __init__(self, description: str, user_options: list, dist, **kw):
        # """

        # Args:
            # description:
            # user_options:
            # dist:
            # **kw:
        # """
        # super().__init__(dist, **kw)
        # self.description: str = description
        # self.user_options: list = user_options


# setup(
        # name = NAME,
        # version = about['__version__'],
        # description = DESCRIPTION,
        # long_description_content_type = 'text/markdown',
        # long_description = long_description,
        # author = AUTHOR,
        # author_email = EMAIL,
        # python_requires = REQUIRES_PYTHON,
        # url = URL,
        # #namespace_packages = NAMESPACES,
        # #packages = PACKAGES,
        # #py_modules = PY_MODULES,
        # #entry_points = {
                # 'console_scripts':['LRphase=LRphase:main'],
                # },
        # install_requires = REQUIRED,
        # include_package_data = True,
        # packages=find_packages('src'),
        # package_dir={'': 'src'},
        # package_data=
        # {
        # '': ['data/error_tables/*'],
        # },
        # py_modules = ['LRphase','InputData','SimulatePhasedData','PhasableSample','PhasedRead','PhaseSet','HeterozygousSites'],
        # entry_points={'console_scripts': ['LRphase = LRphase:main']},
        # license = LICENSE,
        # classifiers = [
                # # Trove classifiers
                # # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
                # 'License :: OSI Approved :: MIT License',
                # 'Programming Language :: Python',
                # 'Programming Language :: Python :: 3',
                # 'Programming Language :: Python :: 3.6',
                # 'Programming Language :: Python :: 3.7',
                # 'Programming Language :: Python :: 3.8',
                # 'Programming Language :: Python :: 3.9',
                # 'Programming Language :: Python :: Implementation :: CPython',
                # 'Programming Language :: Python :: Implementation :: PyPy',
                # 'Intended Audience :: Science/Research',
                # 'Natural Language :: English',
                # 'Operating System :: Microsoft',
                # 'Operating System :: MacOS',
                # 'Operating System :: Unix',
                # 'Programming Language :: Python',
                # 'Topic :: Documentation',
                # 'Topic :: Scientific/Engineering :: Bio-Informatics',
                # 'Topic :: Software Development :: Libraries :: Python Modules',
                # 'Topic :: Software Development :: Version Control :: Git'
                
                # ],
        # # $ setup.py publish support.
        # cmdclass = {
                # 'upload':UploadCommand,
                # },
        # )
