#!/usr/bin/env python3
"""
help.py

This is a file to pull the help for all programs in bin. Each script must be
 added individually, some scripts use argparse, so -h is called, others do not,
 and so their __doc__ is printed. Based on spHelp written by Elena.

2020-06-08  DG  Init, based on spHelp
2020-08-17  DG  Added XMID and WAVEMID
2020-10-18  DG  Added m4l
"""
import subprocess as sub
from pathlib import Path
from bin import sjd, sp_version, m4l

__version__ = '3.1.0'

argparsed = ['ap_test.py', 'boss_sha1sum.py', 'ds9_live.py', 'epics_fetch.py',
             'get_dust.py', 'sloan_log.py', 'tpm_fetch.py', 'tpm_feed.py']
non_argparsed = ['sjd.py', 'sp_version.py', 'wave_mid.py', 'x_mid']
bin_dir = Path(__file__).parent

for arg in argparsed:
    print('{:=^80}'.format(arg))
    sub.call([bin_dir / arg, '-h'])
    print()

# These scripts don't use argparse, but they do have a docstring and a main
# function, so they can be safely imported and we'll just print __doc__
print('{:=^80}'.format('sjd.py'))
print(sjd.__doc__)
print('{:=^80}'.format('sp_version.py'))
print(sp_version.__doc__)
print('{:=^80}'.format('m4l.py'))
print(m4l.__doc__)

# Because these files don't have a main syntax, we can't import them and print
# __doc__, so we have to read them manually
wavemid = open(bin_dir / 'wave_mid.py', 'r').read()
print('{:=^80}'.format('wave_mid.py'))
print(wavemid.split('"""')[1])

xmid = open(bin_dir / 'x_mid.py', 'r').read()
print('{:=^80}'.format('x_mid.py'))
print(xmid.split('"""')[1])
