Sphinx Docs
===========

This repository is enabled with Sphinx documentation for the Python
modules.

Setting up Sphinx
-----------------

To work on the Sphinx docs for this package you must have Sphinx
installed on your system or in your virtual environment (``virtualenv``
is recommended).

Building and publishing
-----------------------

The Sphinx documentation source files are reStructuredText files, and
are contained in the ``docs/source`` sub-folder. ``docs`` also contains the ``Makefile``
for the build. To do a new build make sure you are in the ``docs`` sub-folder
and run

::

    make html

You should see a new set of HTML files and assets in the ``docs/build/html``
sub-folder (the build directory can be changed to ``docs`` itself in the
``Makefile`` but that is not recommended).

..
    commented-out:: The ``docs`` sub-folder should always contain the latest copy of the built
    HTML and assets so first copy the files from ``docs/build/html`` to ``docs`` using

    ::

        cp -R _build/html/* .

    Add and commit these files to the local repository, and then update the
    remote repository on GitHub.