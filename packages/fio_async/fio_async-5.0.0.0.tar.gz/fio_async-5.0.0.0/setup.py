#!/usr/bin/env python3
import re
import os
import sys
import time
import unittest
from configparser import ConfigParser
from setuptools import setup, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PostgresTest(Command):
    """
    Run the tests on Postgres.
    """
    description = "Run tests on Postgresql"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.environ['DB_NAME'] = 'test_' + str(int(time.time()))
        os.environ['TRYTOND_DATABASE_URI'] = "postgresql://"
        os.environ['TRYTOND_ASYNC__BROKER_URL'] = "redis://localhost:6379/0"
        os.environ['TRYTOND_ASYNC__BACKEND_URL'] = "redis://localhost:6379/1"

        from tests import suite

        test_result = unittest.TextTestRunner(verbosity=3).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-1)


config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = [
    'wrapt',
    'celery',
]

MODULE2PREFIX = {}

MODULE = "async"
PREFIX = "fio"
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append(
            '%s_%s >= %s.%s, < %s.%s' % (
                MODULE2PREFIX.get(dep, 'trytond'), dep,
                major_version, minor_version, major_version,
                minor_version + 1
            )
        )
requires.append(
    'trytond >= %s.%s, < %s.%s' % (
        major_version, minor_version, major_version, minor_version + 1
    )
)
setup(
    name='%s_%s' % (PREFIX, MODULE),
    version=info.get('version', '0.0.1'),
    description="Execute Tryton methods asynchronously",
    author="Fulfil.IO Inc.",
    author_email='support@fulfil.io',
    url='https://www.fulfil.io/',
    package_dir={
        'trytond_async': '.',
        'trytond.modules.%s' % MODULE: '.'
    },
    packages=[
        'trytond_async',    # Another package alias for easy import of task
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
    ],
    package_data={
        'trytond.modules.%s' % MODULE: info.get('xml', []) +
        info.get('translation', []) +
        ['tryton.cfg', 'locale/*.po', 'tests/*.rst', 'reports/*.odt'] +
        ['view/*.xml'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Tryton',
        'Topic :: Office/Business',
    ],
    license='BSD',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    cmdclass={
        'test': PostgresTest,
    }
)
