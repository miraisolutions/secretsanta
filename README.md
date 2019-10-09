# secretsanta
This repository implements a basic Python version of a *secret santa* utility. It is meant to serve as a tutorial for beginners interested in Python package development.

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)
[![PyPI](https://img.shields.io/pypi/v/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/secretsanta.svg)](https://pypistats.org/packages/secretsanta)
[![PyPI - License](https://img.shields.io/pypi/l/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)

[![Build Status](https://travis-ci.org/miraisolutions/secretsanta.svg?branch=master)](https://travis-ci.org/miraisolutions/secretsanta)
[![codecov](https://codecov.io/gh/miraisolutions/secretsanta/branch/master/graph/badge.svg)](https://codecov.io/gh/miraisolutions/secretsanta)

### Development

We assume **PyCharm** on **Ubuntu >= 16.04** as the development environment.

In PyCharm, check out this repository into a new project, e.g. using menu `VCS > Checkout from Version Control`.

Shell commands below should be entered in the **Terminal** pane of PyCharm.

[//]: # "See https://stackoverflow.com/questions/4823468/comments-in-markdown" 
[//]: # "Sorry but there is no shortcut in PyCharm to send code to the terminal..."  
[//]: # "(I tried both *Quick Lists* and *Macros* but neither seems exactly fit for this purpose.)"

#### Virtual environments

We'll use a virtual environment to keep things neat and tidy (and you don't want to be [Mr. Messy](https://mrmen.fandom.com/wiki/Mr._Messy), now do you).  
A couple of useful references about virtual environments if you've never used them before:
* <https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>
* <https://docs.python-guide.org/dev/virtualenvs/>

Install support for virtual environments with Python 3.x if you don't have it yet:
```bash
sudo apt-get install python3-venv
```

Configure the PyCharm project with a Python 3 virtual environment under
```
File > Settings > Project > Project interpreter
```
Click on the top-right *gear* icon and select `Add...`, then create a new `Virtualenv Environment`, using `<PROJECT_PATH>/venv` 
as location and Python 3.x as interpreter. Also un-tick all checkboxes.

_We do not use `pipenv` here. You may however use it to create a new environment 
[in the same way](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project)._

With these settings, anything you execute within the PyCharm project, either at the Terminal or in the Python Console, 
will run in the virtual environment. Close and re-open PyCharm to make sure the settings are picked up.

Note that you can still temporarily leave the virtual environment from an active Terminal using command
```bash
deactivate
```
and re-activate it using
```bash
source ./venv/bin/activate
```
You can also switch to a different project interpreter in PyCharm (Ctrl + Shift + A, search for _Switch Project Interpreter_).
Open terminals and Python consoles then need to be restarted for the environment to match the project interpreter.

#### Project requirements

The project includes files `requirements.in` and `requirements-package.in`, defining module / package dependencies. 
Such files are compiled into an actual `requirements.txt` file, which is not committed to Git and should be re-created for the local checkout.

NOTE: make sure all commands are executed inside the virtual environment, e.g. at such a prompt:
```
#> (venv) mirai@MiraiUbuntu:~/PycharmProjects/secretsanta$
```

Check version of Python:
```bash
python --version
```

Upgrade `pip`
```bash
pip install --upgrade pip
```

Check version of pip:
```bash
pip --version
#> pip 18.1 from /home/mirai/PycharmProjects/secretsanta/venv/lib/python3.5/site-packages/pip (python 3.5)
```

Install `pip-tools`:
```bash
pip install pip-tools
```
(<https://github.com/jazzband/pip-tools>)

List installed modules:
```{bash, eval=FALSE}
pip list
```
```
#> Package       Version
#> ------------- -------
#> Click         7.0    
#> pip           18.1   
#> pip-tools     3.1.0  
#> pkg-resources 0.0.0  
#> setuptools    20.7.0 
#> six           1.11.0 
```

Re-generate `requirements.txt` from `requirements.in`:
```{bash, eval=FALSE}
pip-compile
```
You can right-click on the `secretsanta` project folder in the `Project` explorer and click
**Synchronize 'secretsanta'** to refresh and see the generated file `requirements.txt`.

Install dependencies defined in `requirements.txt`:
```{bash, eval=FALSE}
pip-sync
```

_If you change the virtual environment you work with, you should run `pip-compile -U` and rerun `pip-sync` to make 
sure that compatible versions of your dependencies are used in the new environment._ 

Now you're ready to go. Would there be any update to the requirements `.in` files, make sure you re-execute `pip-compile` and `pip-sync`.

### Testing
Tests are kept under `tests/` and make use of the `unittest` framework.

Run code style checks with flake8:
```{bash, eval=FALSE}
flake8
```
If all is fine, you will not see any output.

Run tests for multiple Python versions, using `tox` (<https://tox.readthedocs.io/en/latest/>):
```{bash, eval=FALSE}
tox
```
See `tox.ini` (where the Python versions to test with are defined) for `tox`, `pytest` (which is used as a test runner) 
and `flake8` configuration.

Coverage is measured and reported using the `pytest-cov` package.
The related configuration resides in `tox.ini` and `.coveragerc`.

_The tests will only be run for any Python version that is available in the environment where you run them. 
(See `skip_missing_interpreters` configuration key)_

In PyCharm, you can associate files to a certain type under:
```
File > Settings > Editor > File Types
```
E.g. use this to get `.coveragerc` marked up as `INI` (you can do this after installing the .ini support PyCharm plugin).
Alternatively, you can register the `*.ini` and `.coveragerc` patterns to the *existing* 'Buildout Config' file type [](https://intellij-support.jetbrains.com/hc/en-us/community/posts/206585245/comments/205965729).

### Documentation
Documentation is done using [Sphinx](http://www.sphinx-doc.org/en/master/usage/quickstart.html).

Prerequisite: Installation. Open a terminal (outside of a virtual environment) and run below command:
```{bash, eval=FALSE}
sudo apt-get install python3-sphinx
```
Check installation (and version):
```{bash, eval=FALSE}
sphinx-build --version
```

##### Initializing documentation - already done - for reference:
```{bash, eval=FALSE}
sphinx-quickstart
```
This will lead through an interactive generation process.

Suggested values / options are listed here.
Hitting enter without typing anything will take the suggested default shown inside square brackets [ ].
* Root path for the documentation: docs
* Separate source and build directories: y
* Source file suffix: .rst
* Sphinx extensions: autodoc, doctest, intersphinx, coverage, mathjax, viewcode
* Create Makefile: y

In order to use `autodoc`, one needs to uncomment the corresponding line in `docs/source/conf.py`:

```sys.path.insert(0, os.path.abspath(...```

And set the appropriate path to the directory containing the modules to be documented.

##### Building docs
You should be inside the documentation root directory.  
Using the Makefile:
```bash
cd docs
make html
```
You can view the documentation by opening `index.html` (`docs/build/html`) in your browser of choice.
Previewing the .rst files does not work properly in PyCharm, apparently because 
[it only supports a subset of Sphinx](https://stackoverflow.com/questions/53130720/sphinx-unknown-directive-type-toctree-error-in-pycharm-but-index-html-works).

Alternative build without Makefile:
```bash
sphinx-build -b html <sourcedir> <builddir>
```
PDF output:
```bash
make latexpdf
```

### Usage
The `Jupyter` notebook `SecretSanta.ipynb` illustrates the usage of the `secretsanta` package.

It can be run either directly in PyCharm or maybe more typically in your browser:
```bash
jupyter notebook SecretSanta.ipynb
```

Below gives you some useful information about the location of `Jupyter` related directories, e.g. configuration:
```bash
jupyter --path
```

<!-- `etc/jupyter/custom/custom.js` -->

A few additional links to some typical early `Jupyter` topics:
* [Closing running Jupyter notebook servers](https://github.com/jupyter/notebook/issues/2844)
* [Checkpoints and autosave](https://groups.google.com/forum/#!topic/jupyter/DGCKE5fS4kQ)

### Miscellaneous
* `MANIFEST.in` specifies extra files that shall be included in a source distribution.

* `.travis.yml` is untested and not being used currently, since private repositories require a paid plan.

* `.codecov.yml` is similarly untested and unused, since Travis CI is not set up.  
Note that this file also exposes a webhook URL into Slack, which ideally shouldn't be shared publicly.


##### autodoc notes
For Sphinx/autodoc to work, the docstrings must of course be written in correct 
[reStructuredText](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).
You can then use all of the usual Sphinx markup in the docstrings, and it will end up correctly in the documentation. 
Together with hand-written documentation, this technique eases the pain of having to maintain two locations for
documentation, while at the same time avoiding auto-generated-looking pure API documentation.

For more on autodoc see <http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc>.

The main autodoc features used in this documentation are:

    .. automodule:: <module_name>
    .. autoclass:: <class_name> and
    .. autofunction:: <function_name>

The key to using these features is the :members: attribute. If:

* You don’t include it at all, only the docstring for the object is brought in;
* You just use `:members:` with no arguments, then all public functions, classes, and methods that have a docstring are brought in;
* You explicitly list the members like `:members: fn0, class0, _fn1`, those explicit members are brought in.

[//]: # "TODO Is the below still required ?" 

We’ll examine these points in the full example "Full Code Example" (<https://pythonhosted.org/an_example_pypi_project/sphinx.html>).
