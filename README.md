# About

MacTimeLog is a simple time tracking tool for Mac OS X.

To build MacTimeLog run:

    python setup.py py2app


# Development

To build MacTimeLog during development use SCons script which builds only things
that changed, hence it's much faster than py2app approach
([SCons](http://www.scons.org) tool is requred for that):

    scons

To build MacTimeLog that uses differnet application support
directory - MacTimeLogDev (allows you to have separate settings and log file
for testing) use `debug=1` param:

    scons debug=1
