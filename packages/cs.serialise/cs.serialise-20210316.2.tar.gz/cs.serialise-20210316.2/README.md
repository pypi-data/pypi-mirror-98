OBSOLETE: some serialising functions. Please use by cs.binary instead.

*Latest release 20210316.2*:
Further obsolescence: drop tests, mark as Development Status :: 7.

Porting guide:
* `get_bs` is now `BSUInt.parse_bytes`.
* `put_bs` is now `BSUInt.transcribe_value`.

# Release Log



*Release 20210316.2*:
Further obsolescence: drop tests, mark as Development Status :: 7.

*Release 20210316.1*:
Still obsolete (use cs.binary) but do not raise ImportError, just print a warning to sys.stderr.

*Release 20210316*:
* Make obviously obsolete, yea, even unto raising an ImportError on import.
* Point users as cs.binary instead.

*Release 20190103*:
Move most code into cs.binary, leave compatibility names behind here.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Redo entire API with saner names and regular interface, add unit tests.
* Implement general purpose Packet class.
* Add put_bss, get_bss, read_bss to serialise strings.
* Python 2/3 port fix.
* DOcstring improvements and other internal improvements.

*Release 20150116*:
Initial PyPI release.
