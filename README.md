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
    b. [Project requirements](#project-requirements)  
2. [Testing](#testing)  
    a. [PyCharm file types](#pycharm-file-types)  
    b. [Type hints](#type-hints)  
    c. [Property testing](#property-testing)  
    d. [Mocks in unit tests](#mocks-in-unit-tests)  
3. [Documentation](#documentation)  
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
```
File > Settings > Project > Project interpreter
```
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

#### Project requirements

The project includes files `requirements.in` and `requirements-package.in`, defining module / package dependencies. 
Such files are compiled into an actual `requirements.txt` file,
which is not committed to Git and should be re-created for the local checkout.

**Important:** make sure all commands are executed inside the virtual environment, e.g. at such a prompt:
```
#> (venv) localuser@Ubuntu:~/PyCharm/secretsanta$
```

Check version of Python, upgrade [pip](https://pypi.org/project/pip/) and check its version:
```bash
python --version
#> Python 3.6.8

pip install --upgrade pip
#> ...

pip --version
#> pip 20.3.3 from /home/mirai/PycharmProjects/secretsanta/venv/lib/python3.8/site-packages/pip (python 3.8)
```

Install [pip-tools](<https://github.com/jazzband/pip-tools>):
```bash
pip install pip-tools
```

List installed modules:
```{bash, eval=FALSE}
pip list
#> Package       Version
#> ------------- -------
#> Click         7.0    
#> pip           21.0.1 
#> pip-tools     5.5-0
#> pkg-resources 0.0.0  
#> setuptools    51.0.0 
#> six           1.15.0 
```

Re-generate `requirements.txt` from `requirements.in`:
```{bash, eval=FALSE}
pip-compile
```
Install dependencies defined in `requirements.txt`:
```{bash, eval=FALSE}
pip-sync
```
*Alternatively, you can right-click on the `secretsanta` project folder in the `Project` explorer and click
**Synchronize 'secretsanta'** to refresh and see the generated file `requirements.txt`.*

Now you're ready to go. Would there be any update to the `requirements.in` files,
make sure you re-execute `pip-compile` and `pip-sync`.

*If you change the virtual environment you work with, you should instead run `pip-compile -U` (then
rerun `pip-sync`) to make sure that compatible versions of your dependencies are used in the new environment.*

### Testing
There are multiple ways to define and execute tests. Two of the most common ones are `doctest` and `unittest`.

The `doctest` module allows to run code examples / tests that are defined as part of `docstrings`.

Use the following command to see this in action. The `-v` flag allows us to see verbose output.
In case everything is fine, we would not see any output otherwise.
```{bash, eval=FALSE}
python -m doctest secretsanta/main/core.py -v
```

It is possible to run code style checks with [flake8](http://flake8.pycqa.org/en/latest/):
```{bash, eval=FALSE}
flake8
```
If all is fine, you will not see any output.

Unit tests are kept under `tests` and make use of the `unittest` framework.

Run tests using [tox](<https://tox.readthedocs.io/en/latest/>):
```{bash, eval=FALSE}
tox
```
The `tox.ini` file contains the following configurations:
* `flake8` (checks code style and reports potential issues)
* `pytest` (which is used as a test runner)
* `pytest-cov` (measures and reports test coverage, see also `.coveragerc` file)
* `tox` (where the Python versions to test with are defined)

If you run `tox` outside of the virtual environment, it can run tests for multiple Python versions - this is configured
using `envlist`.The tests will only be run for any Python version that is available in the environment where you run them
(see `skip_missing_interpreters` configuration key).

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

mypy comes installed in the virtual environment as it's part of requirements.in.

Run something like below:
```{bash, eval=FALSE}
mypy ./secretsanta/main/core.py
mypy ./tests
mypy .
```
to test if the type hints of `.py` file(s) are correct (in which case it would typically output a "Success" message).

#### Property testing
We use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) to define a _property test_ for our matching function: 
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

##### Building docs
You should be inside the documentation root directory.  
Using the Makefile:

```bash
cd docs
make html
```
You can view the documentation by right-click opening `index.html` (`docs/build/html`) in your browser of choice.
Previewing the .rst files does not work properly in PyCharm, apparently because 
[it only supports a subset of Sphinx](https://stackoverflow.com/questions/53130720/sphinx-unknown-directive-type-toctree-error-in-pycharm-but-index-html-works).

Alternative build without Makefile:
```bash
sphinx-build -b html <sourcedir> <builddir>
```

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

In order to install the package and **run the CLI commands**, you can follow the steps below.
- On **Windows**, set `PYTHONPATH` to point to this project by adding it to environment variables in PyCharm (`File > Settings... > Terminal > Environment variables`). On **Ubuntu**, export it via command line instead: `export PYTHONPATH=$PYTHONPATH:<path to secretsanta project>`. Then run:
```bash
python secretsanta/cli/cli.py --help
```
- try a specific command:
```bash
python secretsanta/cli/cli.py makedict --help
python secretsanta/cli/cli.py makedict "./validation/participants.json"
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

This repository uses [Travis CI](https://travis-ci.com) to run tests automatically when new commits are pushed. Results
can be viewed [here](https://travis-ci.com/miraisolutions/secretsanta). Along with test results,
coverage information is generated and uploaded to [codecov](https://codecov.io/), which generates a
[report](https://codecov.io/gh/miraisolutions/secretsanta) out of it.

#### Configuration
Travis CI is configured using the `.travis.yml` file. This allows specifying the environment(s) to run
tests in; tests will be run for each specified environment. The steps required before running tests are specified under
`install`. Finally, the task to run is defined in `script`, and we make sure coverage reports are uploaded (see
`after_success`). A notification about completed builds is sent to our Slack channel using a
[secure notification hook](https://docs.travis-ci.com/user/notifications/#configuring-slack-notifications).

Codecov is configured in `codecov.yml`, defining the coverage value range (in percent) to match to a color scale, as
well as the coverage checks to be performed and their success criteria. See codecov's
[general configuration](https://docs.codecov.io/docs/codecov-yaml) and
[commit status evaluation](https://docs.codecov.io/docs/commit-status) documentation for more information.

_Notifications from codecov can only be delivered via unencrypted webhook URLs. In order to avoid exposing such hooks in
a public repository, we do not use this functionality here._

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
