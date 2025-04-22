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

The Sphinx documentation source files are ``reStructuredText`` files, and
are contained in the ``docs/source`` sub-folder.

To build the documentation, ensure you have set up your development environment
(see main README) and run the `docs` session using Nox:

::

    nox -s docs

This command uses `sphinx-build` to generate the HTML output.

You should see a new set of HTML files and assets in the ``docs/build/html``
sub-folder. Open `docs/build/html/index.html` in your browser to view the docs.

..
    commented-out:: The ``docs`` sub-folder should always contain the latest copy of the built
    HTML and assets so first copy the files from ``docs/build/html`` to ``docs`` using

    ::

        cp -R _build/html/* .

    Add and commit these files to the local repository, and then update the
    remote repository on GitHub.
