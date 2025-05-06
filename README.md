# secretsanta

This repository implements a basic Python version of a [Secret Santa](https://en.wikipedia.org/wiki/Secret_Santa)
utility. It is meant to serve as a tutorial for beginners interested in Python package development.
Each section below mentions typical tools and utilities in a natural order of developing Python packages.

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)
[![PyPI](https://img.shields.io/pypi/v/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/secretsanta.svg)](https://pypistats.org/packages/secretsanta)
[![PyPI - License](https://img.shields.io/pypi/l/secretsanta.svg)](https://pypi.python.org/pypi/secretsanta)

[![Build Status](https://github.com/miraisolutions/secretsanta/actions/workflows/python-package.yml/badge.svg)](https://github.com/miraisolutions/secretsanta/actions/workflows/python-package.yml)

[![codecov](https://codecov.io/gh/miraisolutions/secretsanta/branch/master/graph/badge.svg)](https://codecov.io/gh/miraisolutions/secretsanta)

### Table of Contents

1. [Development](#development)  
    a. [Virtual environments](#virtual-environments)  
    b. [Project requirements & Environment Setup](#project-requirements--environment-setup)  
2. [Testing](#testing)  
    a. [Running Tests with Nox](#running-tests-with-nox)  
    b. [PyCharm file types](#pycharm-file-types)  
    c. [Type hints](#type-hints)
    d. [Property testing](#property-testing)  
    e. [Mocks in unit tests](#mocks-in-unit-tests)  
3. [Documentation](#documentation)  
    a. [Building Docs with Nox](#building-docs-with-nox)  
4. [Usage](#usage)  
    a. [Jupyter notebook](#jupyter-notebook)  
    b. [Command-line interface](#command-line-interface-cli)  
    c. [Package installation & CLI](#package-installation--cli)  
5. [Continuous integration](#continuous-integration)  
6. [Miscellaneous](#miscellaneous)  

### Development

We assume **PyCharm** on **Ubuntu >= 20.04** as the development environment, but you might as well use a newer Linux version or even Windows instead.

In PyCharm, check out this repository into a new project, e.g. under

```
VCS > Checkout from Version Control
```

Shell commands below should be entered in the **Terminal** pane of PyCharm.

*There is no shortcut in PyCharm to send code from the editor to the terminal, so you need to copy-paste commands instead.*

[//]: # "(I tried both *Quick Lists* and *Macros* but neither seems exactly fit for this purpose.)"
[//]: # "This is a comment. See https://stackoverflow.com/questions/4823468/comments-in-markdown"

#### Virtual environments

We'll use a virtual environment to keep things neat and tidy.  
A couple of useful references about virtual environments if you've never used them before:

* [Virtual environments](https://docs.python-guide.org/dev/virtualenvs/)
* [Creating virtual environments](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)

Install support for virtual environments with Python 3.x if you don't have it yet. Below we assume Python 3.8:

```bash
sudo apt-get install python3.8-venv
```

Note that Ubuntu 22.04 does not provide 3.8 (nor 3.9) by default. It can be installed by adding the
[deadsnakes](https://github.com/deadsnakes) repository first to `apt`.

Configure the PyCharm project with a Python 3.8 virtual environment under

`File > Settings > Project > Project interpreter`

Click on the top-right *gear* icon and select `Add...`, then create a new `Virtualenv Environment`, using `<PROJECT_PATH>/venv`
as location and Python 3.x as interpreter. Also un-tick all checkboxes.

*We do not use `pipenv` here. You may however use it to create a new environment
[in the same way](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project).*

With these settings, anything you execute within the PyCharm project, either at the Terminal or in the Python Console,
will run in the virtual environment. Close and re-open PyCharm to make sure the settings are picked up.

Note that you can still temporarily leave the virtual environment from an active Terminal using

```bash
deactivate
```

and re-activate it using

```bash
source ./venv/bin/activate
```

You can also switch to a different project interpreter in PyCharm (Ctrl + Shift + A, search for `Switch Project Interpreter`).
Open terminals and Python consoles then need to be restarted for the environment to match the project interpreter.

#### Project requirements & Environment Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and [Nox](https://nox.thea.codes/) for task automation and testing across multiple Python versions.

**Important:** make sure all commands are executed inside the virtual environment, e.g. at such a prompt:

```bash
#> (venv) localuser@Ubuntu:~/PyCharm/secretsanta$
```

First, ensure you have `uv` installed. You can install them into your global Python environment or use `pipx`:

```bash
pip install uv
# or
pipx install uv
```

Check version of `uv`:

```bash
uv --version
```

To set up your development environment, synchronize it with the locked dependencies specified in `uv.lock`:

```bash
# Install runtime, dev, test, and docs dependencies
uv sync --all-extras --dev
```

If you modify dependencies in `pyproject.toml`, update the lock file:

```bash
uv lock
```

Then re-sync your environment:

```bash
uv sync --all-extras --dev
```

You can also run commands within the managed environment using `uv run`:

```bash
uv run -- python secretsanta/cli/cli.py --help
```

### Testing

There are multiple ways to define and execute tests. Two of the most common ones are `doctest` and `unittest`.

The `doctest` module allows to run code examples / tests that are defined as part of `docstrings`.

Use the following command to see this in action. The `-v` flag allows us to see verbose output.
In case everything is fine, we would not see any output otherwise.

```{bash, eval=FALSE}
python -m doctest secretsanta/main/core.py -v
# Or run via nox (included in the 'tests' session)
uv run nox -s tests -- -m doctest secretsanta/main/core.py -v
```

It is possible to run code style checks with [flake8](http://flake8.pycqa.org/en/latest/):

```{bash, eval=FALSE}
# Run directly
flake8 secretsanta tests
# Or run via nox
uv run nox -s lint
```

If all is fine, you will not see any output from `flake8` directly. `nox` will report success.

Unit tests are kept under `tests`.

#### Running Tests with Nox

[Nox](https://nox.thea.codes/) is used to automate testing across multiple Python versions (defined in `noxfile.py`).

List available Nox sessions:

```bash
uv run nox --list
```

Run all test sessions (for Python 3.8, 3.9, 3.10, 3.11, 3.12):

```bash
uv run nox -s tests
```

Run tests for a specific Python version:

```bash
uv run nox -s tests-3.10
```

Run linting session:

```bash
uv run nox -s lint
```

Run all sessions:

```bash
uv run nox
```

Nox handles creating temporary virtual environments for each session, installing dependencies using `uv`, and running the specified commands. Test coverage is measured using `pytest-cov` (see `.coveragerc` and `pyproject.toml` for configuration).

#### PyCharm file types

In PyCharm, you can associate files to a certain type under:

```
File > Settings > Editor > File Types
```

E.g. use this to get `.coveragerc` marked up as `INI` (you can do this after installing the .ini support PyCharm plugin).
Alternatively, you can register the `*.ini` and `.coveragerc` patterns to the *existing* **Buildout Config**
[file type](https://intellij-support.jetbrains.com/hc/en-us/community/posts/206585245/comments/205965729).

#### Type hints

Type hints define what type function arguments and return values should be. They are both a source of documentation
and testing framework to identify bugs more easily, see also [PEP 484](https://www.python.org/dev/peps/pep-0484/).

mypy comes installed via `uv sync --dev`.

Run something like below:

```{bash, eval=FALSE}
mypy ./secretsanta/main/core.py
mypy ./tests
mypy .
# Or run via nox (if a session is added)
# nox -s typecheck
```

to test if the type hints of `.py` file(s) are correct (in which case it would typically output a "Success" message).

#### Property testing

We use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) to define a *property test* for our matching function:
generated example inputs are tested against desired properties. Hypothesis' generator can be configured to produce typical
data structures, filled with various instances of primitive types. This is done by composing specific annotations.

* The decorator `@given(...)` must be present before the test function that shall use generated input.
* Generated arguments are defined in a comma-separated list, and will be passed to the test function in order:

```python
from hypothesis import given
from hypothesis.strategies import text, integers


@given(text(), integers())
def test_some_thing(a_string, an_int):
    return

```  

* Generation can be controlled by various optional parameters, e.g. `text(min_size=2)` for testing with strings that
have at least 2 characters.

#### Mocks in unit tests

Mock objects are used to avoid external side effects. We use the standard Python package `unittest.mock`. This provides
a `@patch` decorator, which allows us to specify classes to be mocked within the scope of a given test case. See
*test_funs.py* and *test_core.py* for examples.

### Documentation

Documentation is done using [Sphinx](http://www.sphinx-doc.org/en/master/usage/quickstart.html). We use Google style docstrings as that seems to be prevalent in the industry,
with the addition of `napoleon` Sphinx extension.

Dependencies (like Sphinx) are installed via `uv sync --all-extras`.

#### Initializing documentation - already done - for reference

```{bash, eval=FALSE}
sphinx-quickstart
```

This will lead through an interactive generation process.

Suggested values / options are listed here.
Hitting enter without typing anything will take the suggested default shown inside square brackets [ ].

* Root path for the documentation [.]: docs
* Separate source and build directories (y/n) [n]: y
* Name prefix for templates and static dir[_]: Enter
* Project name: secretsanta
* Author name(s): Mirai Solutions
* Project version[]: 0.1
* Project release[0.1]: 0.1.1
* Project language [en]: None
* Source file suffix [.rst]: .rst
* Name of your master document (without suffix) [index]: Enter
* Do you want to use epub builder (y/n) [n]: n
* autodoc: automatically insert docstrings from modules (y/n) [n]: y
* doctest: automatically test code snippets in doctest blocks (y/n) [n]: y
* intersphinx: link between Sphinx documentation of different projects (y/n) [n]: y
* todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: n
* coverage: checks for documentation coverage (y/n) [n]: y
* imgmath: include math, rendered as PNG or SVG images (y/n) [n]: n
* mathjax: include math, rendered in the browser by MathJax (y/n) [n]: y
* ifconfig: conditional inclusion of content based on config values (y/n) [n]: n
* viewcode: include links to the source code of documented Python objects (y/n) [n]: y
* githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: n
* Create Makefile? (y/n) [y]: y
* Create Windows command file? (y/n) [y]: n

In order to use `autodoc`, one needs to uncomment the corresponding line in `docs/source/conf.py`:

```sys.path.insert(0, os.path.abspath(...```

And set the appropriate path to the directory containing the modules to be documented.

*For Sphinx/autodoc to work, the docstrings must be written in correct
[reStructuredText](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html),
see [documentation](https://pythonhosted.org/an_example_pypi_project/sphinx.html#auto-directives) for details.*

#### Building Docs with Nox

Use Nox to build the documentation:

```bash
uv run nox -s docs
```

This command runs `sphinx-build` in a dedicated environment managed by Nox.

You can view the documentation by opening `docs/build/html/index.html` in your browser.

*Previewing the .rst files directly in PyCharm might not render Sphinx directives correctly.*

### Usage

#### Jupyter Notebook

The [Jupyter](https://jupyter.org/) notebook `SecretSanta.ipynb` illustrates the usage of the `secretsanta` package.

It can be run in your browser (or directly in PyCharm if you have the professional edition):

```bash
jupyter notebook SecretSanta.ipynb
```

Below gives you some useful information about the location of `Jupyter` related directories, e.g. configuration:

```bash
jupyter --path
```

<!-- e.g.: `etc/jupyter/custom/custom.js` -->

A few additional links to some typical early `Jupyter` topics:

* [Closing running Jupyter notebook servers](https://github.com/jupyter/notebook/issues/2844)
* [Checkpoints and autosave](https://groups.google.com/forum/#!topic/jupyter/DGCKE5fS4kQ)

#### Command-line Interface (CLI)

Python's ecosystem offers several ways to tackle command-line interfaces. The traditional standard method is to use
the `argparse` module that is part of the standard library. This can be complemented by something like `argparsetree`
for larger and more complex command-line applications.

Here we have chosen to use [Click](https://click.palletsprojects.com/) instead, which allows us to define our CLI via
decorated functions in a neat and compact way. Other potential alternatives could
be [docopt](https://docopt.readthedocs.io/) or [Invoke](https://www.pyinvoke.org/).

A nice comparison is
available [here](https://realpython.com/comparing-python-command-line-parsing-libraries-argparse-docopt-click/).

In order to run the CLI commands during development, use `uv run`:

```bash
uv run -- santa --help
uv run -- santa makedict --help
uv run -- santa makedict "./validation/participants.json"
```

Alternatively, activate your virtual environment (where dependencies are installed via `uv sync`) and run directly:

```bash
# Assuming your venv is activated
santa --help
santa makedict "./validation/participants.json"
```

#### Package Installation & CLI

If you install the package, you can use the CLI tool as designed for the end user:

```bash
python -m pip install --upgrade pip

pip install --upgrade build

python -m build  # creates build and dist directories

# Windows:
pip install .\dist\secretsanta-0.1.0-py3-none-any.whl
# if already installed, use below to force re-installation:
pip install --force-reinstall .\dist\secretsanta-0.1.0-py3-none-any.whl

# Ubuntu:
pip install ./dist/secretsanta-0.1.0.tar.gz
# if already installed, use below to force re-installation:
pip install --force-reinstall ./dist/secretsanta-0.1.0.tar.gz

# now you can use the CLI tool properly as below:
santa --help
santa makedict --help
santa makedict "./validation/participants.json"
```

### Continuous Integration

Continuous Integration (CI) aims to keep state updated to always match the code currently checked in a repository.
This typically includes a build, automated test runs, and possibly making sure that the newly built artifacts are
deployed to a target environment. This helps developers and users by providing timely feedback and showing what the
results of certain checks were on a given version of the code.

Coverage information is generated and uploaded to [codecov](https://codecov.io/), which generates a
[report](https://codecov.io/gh/miraisolutions/secretsanta) out of it.

Build status and coverage reports are linked via badges at the top of this README.

Code scanning is performed using CodeQL (see `.github/workflows/codeql.yml`).

Dependency updates are managed by Dependabot (see `.github/dependabot.yml`).

Codecov is configured in `codecov.yml`, defining the coverage value range (in percent) to match to a color scale, as
well as the coverage checks to be performed and their success criteria. See codecov's
[general configuration](https://docs.codecov.io/docs/codecov-yaml) and
[commit status evaluation](https://docs.codecov.io/docs/commit-status) documentation for more information.

*Notifications from codecov can only be delivered via unencrypted webhook URLs. In order to avoid exposing such hooks in
a public repository, we do not use this functionality here.*

### Miscellaneous

* `MANIFEST.in` specifies extra files that shall be included in a source distribution.
* Badges: This README features various badges (at the beginning), including a build status badge and a code coverage
status badge.

##### Logging

The `logging` package is used to track events after running the project. The main logged events (levels) in Secret Santa are: errors, warnings, and participants info. A log level is set as an environment variable, e.g.:

```bash
os.environ["level"] = "ERROR"
```

All logs activities are collected into a log file that is initiated at the beginning of the code:

```bash
logging.basicConfig(filename = path_to_file, level = level, format = '%(asctime)s %(levelname)s %(message)s',
                               datefmt = '%Y/%m/%d %I:%M:%S %p')
```

A logger is then set:

```bash
logger = logging.getLogger(__name__)
```

All functions used afterwards refer to this logger:

```bash
logger.error("Error message")
logger.warning("Warning message")
logger.info("Info")
```

The log file is automatically created in the `log_files` directory and can be inspected after the project run is complete.
