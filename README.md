# secretsanta
Secret Santa Python version

<https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments>

<https://docs.python-guide.org/dev/virtualenvs/>

Open the **Terminal** pane.  
Sorry but there is no shortcut in PyCharm to send code to the terminal...  
(I tried both *Quick Lists* and *Macros* but neither seems exactly fit for this purpose.)

Install support for virtual environments with Python 3.x if you don't have it yet:
```{bash, eval=FALSE}
sudo apt-get install python3-venv
```
Configure project with Python 3 virtual environment:
```{bash, eval=FALSE}
python3 -m venv .
```

Activate virtual environment (same command to re-activate on another session later on).
```{bash, eval=FALSE}
source ./bin/activate
```

Below onwards should be inside the virtual environment, e.g. at such a prompt:
```{bash, eval=FALSE}
#> (secretsanta) mirai@MiraiUbuntu:~/PycharmProjects/secretsanta$
```

Check version of Python:
```{bash, eval=FALSE}
python --version
```

Upgrade pip (don't do this outside the virtual environment!):
```{bash, eval=FALSE}
pip install --upgrade pip
```

Check version of pip:
```{bash, eval=FALSE}
pip --version
#> pip 18.1 from /home/mirai/PycharmProjects/secretsanta/lib/python3.5/site-packages/pip (python 3.5)
```

Install pip-tools:
```{bash, eval=FALSE}
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

Re-generate requirements.txt from requirements.in:
```{bash, eval=FALSE}
pip-compile
```
You can right-click on the `secretsanta` project folder in the `Project` explorer and click
**Synchronize 'secretsanta'** to refresh and see the generated file `requirements.txt`.

Install dependencies defined in `requirements.txt`:
```{bash, eval=FALSE}
pip-sync
```

#### Testing
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
See `tox.ini` for `tox`, `pytest` (which is used as a test runner) and `flake8` configuration.

Coverage is measured and reported using the `pytest-cov` package.
Related configuration resides in `tox.ini` and `.coveragerc`.

In PyCharm, you can associate files to a certain type under:
```
File > Settings > Editor > File Types
```
E.g. use this to get `.coveragerc` marked up as `INI` (.ini support is available through a plugin).

#### Miscellaneous
`MANIFEST.in` specifies extra files that shall be included in a source distribution.

`.travis.yml` is untested and not being used currently, since private repositories require a paid plan.

`.codecov.yml` is similarly untested and unused, since Travis CI is not set up.  
Note that this file also exposes a webhook URL into Slack, which ideally shouldn't be shared publicly.

Leave the virtual environment with the command `deactivate`.
