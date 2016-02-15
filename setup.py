#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2012 Rob Guttman <guttman@alum.mit.edu>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from setuptools import setup, find_packages

PACKAGE = 'TracQuiet'
VERSION = '1.0.2'

extra = {}
try:
    from trac.util.dist  import  get_l10n_cmdclass
    cmdclass = get_l10n_cmdclass()
    if cmdclass:
        extra['cmdclass'] = cmdclass
        extractors = [
            ('**.py',                'python', None),
            ('**/templates/**.html', 'genshi', None),
        ]
        extra['message_extractors'] = {
            'quiet': extractors,
        }
# i18n is implemented to be optional here
except ImportError:
    pass

setup(
    name=PACKAGE,
    version=VERSION,
    description='Toggles quiet (no email) mode for Announcer plugin',
    author="Rob Guttman",
    author_email="guttman@alum.mit.edu",
    license='3-Clause BSD',
    url='https://trac-hacks.org/wiki/QuietPlugin',
    packages=['quiet'],
    package_data={'quiet': ['htdocs/*.js', 'htdocs/*.css', 'htdocs/*.png',
                            'locale/*/LC_MESSAGES/*.mo']},
    entry_points={'trac.plugins': ['quiet.web_ui = quiet.web_ui']},
    **extra
)
