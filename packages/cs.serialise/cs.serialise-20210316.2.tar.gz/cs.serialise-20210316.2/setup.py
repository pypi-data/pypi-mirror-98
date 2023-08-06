#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.serialise',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20210316.2',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  description =
    'OBSOLETE: some serialising functions. Please use by cs.binary instead.',
  long_description =
    ('OBSOLETE: some serialising functions. Please use by cs.binary instead.\n'    
 '\n'    
 '*Latest release 20210316.2*:\n'    
 'Further obsolescence: drop tests, mark as Development Status :: 7.\n'    
 '\n'    
 'Porting guide:\n'    
 '* `get_bs` is now `BSUInt.parse_bytes`.\n'    
 '* `put_bs` is now `BSUInt.transcribe_value`.\n'    
 '\n'    
 '# Release Log\n'    
 '\n'    
 '\n'    
 '\n'    
 '*Release 20210316.2*:\n'    
 'Further obsolescence: drop tests, mark as Development Status :: 7.\n'    
 '\n'    
 '*Release 20210316.1*:\n'    
 'Still obsolete (use cs.binary) but do not raise ImportError, just print a '    
 'warning to sys.stderr.\n'    
 '\n'    
 '*Release 20210316*:\n'    
 '* Make obviously obsolete, yea, even unto raising an ImportError on import.\n'    
 '* Point users as cs.binary instead.\n'    
 '\n'    
 '*Release 20190103*:\n'    
 'Move most code into cs.binary, leave compatibility names behind here.\n'    
 '\n'    
 '*Release 20160828*:\n'    
 '* Use "install_requires" instead of "requires" in DISTINFO.\n'    
 '* Redo entire API with saner names and regular interface, add unit tests.\n'    
 '* Implement general purpose Packet class.\n'    
 '* Add put_bss, get_bss, read_bss to serialise strings.\n'    
 '* Python 2/3 port fix.\n'    
 '* DOcstring improvements and other internal improvements.\n'    
 '\n'    
 '*Release 20150116*:\n'    
 'Initial PyPI release.'),
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 7 - Inactive', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 or later (GPLv3+)',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.serialise'],
)
