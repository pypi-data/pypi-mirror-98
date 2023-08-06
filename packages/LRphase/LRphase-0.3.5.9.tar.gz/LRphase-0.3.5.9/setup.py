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


# python3 -m venv LRphase_env
# source LRphase_env/bin/activate
# python3 -m pip install --upgrade pip setuptools wheel pysam pyliftover biopython twine 
# rm -rf build
# rm -rf src/*.egg-info
# python3 setup.py clean --all sdist bdist_wheel
# twine upload --skip-existing dist/*tar.gz
# tox -e check
# 
# twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip

# rm -rf dist build */*.egg-info *.egg-info
# python3 setup.py sdist
# 

def read(*names, **kwargs):
    """
    Args:
        *names:
        **kwargs:
    """
    with io.open(
            join(dirname(__file__), *names),
            encoding = kwargs.get('encoding', 'utf8')
            ) as fh:
        return fh.read()


setup(
        name = 'LRphase',
        version = '0.3.5.9',
        license = 'MIT',
        description = 'Phasing individual long reads using known haplotype information.',
        long_description = '%s\n%s' % (
                re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
                re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
                ),
        author = 'Greg Farnum',
        author_email = 'gregfar@umich.edu',
        url = 'https://pypi.org/project/LRphase/',
        packages = find_packages('src'),
        package_dir = {'':'src'},
        py_modules = [splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data = True,
        zip_safe = False,
        classifiers = [
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
                ],
        project_urls = {
                'Issue Tracker':'https://github.com/LRphase/LRphase_CLI/issues',
                },
        keywords = [
                'long-reads', 'phasing', 'haplotype',
                ],
        python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
        install_requires = [
                'pysam>=0.15.4', 'biopython>=1.78', 'pyliftover>=0.4', 'setuptools',
                ],
        extras_require = {
                'mappy':['mappy'],
                },
        #setup_requires=[
        #    'pytest-runner',
        #],
        entry_points = {
                'console_scripts':[
                        'LRphase = LRphase.cli:main',
                        ]
                },
        )
