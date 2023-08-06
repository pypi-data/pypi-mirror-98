#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.sh',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210316',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'Convenience functions for constructing shell commands.',
  long_description =
    ('Convenience functions for constructing shell commands\n'    
 '\n'    
 '*Latest release 20210316*:\n'    
 'Minor doc update.\n'    
 '\n'    
 'Functions for safely constructing shell command lines from bare strings.\n'    
 'Somewhat like the inverse of the shlex stdlib module.\n'    
 '\n'    
 'As of Python 3.3 the function `shlex.quote()` does what `quotestr()` does.\n'    
 '\n'    
 'As of Python 3.8 the function `shlex.join()` does what `quotecmd()` does.\n'    
 '\n'    
 '## Function `main_shqstr(argv=None)`\n'    
 '\n'    
 'shqstr: emit shell-quoted form of the command line arguments.\n'    
 '\n'    
 '## Function `quote(args)`\n'    
 '\n'    
 'Quote the supplied strings, return a list of the quoted strings.\n'    
 '\n'    
 'As of Python 3.8 the function `shlex.join()` is available for this.\n'    
 '\n'    
 '## Function `quotecmd(argv)`\n'    
 '\n'    
 'Quote strings, assemble into command string.\n'    
 '\n'    
 '## Function `quotestr(s)`\n'    
 '\n'    
 'Quote a string for use on a shell command line.\n'    
 '\n'    
 'As of Python 3.3 the function `shlex.quote()` is available for this.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210316*:\n'    
 'Minor doc update.\n'    
 '\n'    
 '*Release 20180613*:\n'    
 'Rework quotestr significantly to provide somewhat friendlier quoting, '    
 'include "," in the SAFECHARS.\n'    
 '\n'    
 '*Release 20170903.2*:\n'    
 'bugfix __main__ boilerplate after setuptools workaround\n'    
 '\n'    
 '*Release 20170903.1*:\n'    
 'workaround setuptool\'s slightly dumb console_scripts call of a "main" '    
 'function\n'    
 '\n'    
 '*Release 20170903*:\n'    
 'shqstr command; new quotecmd(argv) function\n'    
 '\n'    
 '*Release 20150118*:\n'    
 'Extend SAFECHARS to include colon.\n'    
 '\n'    
 '*Release 20150111*:\n'    
 'minor cleanup\n'    
 '\n'    
 '*Release 20150107*:\n'    
 'initial standalone public release'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  entry_points = {'console_scripts': ['shqstr = cs.sh:main_shqstr']},
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.sh'],
)
