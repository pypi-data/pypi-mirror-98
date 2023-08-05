
"""Package up pure python version of `treap` module, along with `nest` module."""

import os
import sys
import subprocess

from setuptools import setup

version = '2.0.8'


def is_newer(filename1, filename2):
    """Return True if filename1 is newer than filename2."""
    time1 = os.stat(filename1).st_mtime
    time2 = os.stat(filename2).st_mtime

    if time1 > time2:
        return True
    else:
        return False


def m4_it(infilename, outfilename, define):
    """
    Create outfilename from infilename in a make-like manner.

    If outfilename doesn't exit, create it using m4.
    If outfilename exists but is older than infilename, recreate it using m4.
    """
    build_it = False
    if os.path.exists(outfilename):
        if is_newer(infilename, outfilename):
            # outfilename exists, but is older than infilename, build it
            build_it = True
    else:
        # outfilename does not exist, build it
        build_it = True

    if build_it:
        try:
            subprocess.check_call('m4 -D"%s"=1 < "%s" > "%s"' % (define, infilename, outfilename), shell=True)
        except subprocess.CalledProcessError:
            sys.stderr.write('You need m4 on your path to build this code\n')
            sys.exit(1)


if os.path.exists('../m4_treap.m4'):
    m4_it('../m4_treap.m4', 'py_treap.py', 'py')

# from distutils.core import setup
# from Cython.Build import cythonize

setup(
    name='treap',
    py_modules=[
        'treap',
        'py_treap',
        'nest',
        ],
    version=version,
    description='Python implementation of treaps',
    long_description="""
A set of python modules implementing treaps in pure python is provided.

See also my pyx_treap module, which implements treaps in Cython.

Treaps perform most operations in O(log2(n)) time, and are innately sorted.
They're very nice for keeping a collection of values that needs to
always be sorted, or for optimization problems in which you need to find
the p best values out of q, when p is much smaller than q.

A module is provided for treaps that enforce uniqueness.

Example use:
.. code-block:: python

    >>> import treap
    >>> t = treap.treap()
    >>> for i in range(6):
    ...     t[i] = 2**i
    ...
    >>> list(t)
    [0, 1, 2, 3, 4, 5]
    >>> print(t)
    0                                                         5/319487918/32_
    1                         2/861020069/4__                                                 _______________
    2         1/1135044777/2_                 3/1142319761/8_                 _______________                 _______________
    3 0/1473918015/1_ _______________ _______________ 4/2019165697/16 _______________ _______________ _______________ _______________
    >>> list(t.items())
    [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16), (5, 32)]
    >>>

""",
    author='Daniel Richard Stromberg',
    author_email='strombrg@gmail.com',
    url='http://stromberg.dnsalias.org/~dstromberg/treap/',
    platforms='Cross platform',
    license='Apache v2',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        ],
    )
