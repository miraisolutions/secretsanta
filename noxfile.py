import nox
from nox import session

# load project deps from pyproject.toml
import nox.project

proj = nox.project.load_toml("pyproject.toml")


@session(python=["3.8", "3.9", "3.10", "3.11", "3.12"], venv_backend="uv")
def tests(sess):
    # install runtime + dev deps
    sess.install(".", *proj["project"]["optional-dependencies"]["dev"])
    sess.run("pytest", "--cov=secretsanta")


@session(venv_backend="uv")
def lint(sess):
    sess.install(".", "flake8")
    sess.run("flake8", "secretsanta", "tests")


@session(venv_backend="uv")
def lint_critical(sess):
    sess.install(".", "flake8")
    # stop the build if there are Python syntax errors or undefined names
    sess.run(
        "flake8",
        ".",
        "--count",
        "--select=E9,F63,F7,F82",
        "--show-source",
        "--statistics",
    )


@session(venv_backend="uv")
def lint_style(sess):
    sess.install(".", "flake8")
    # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
    sess.run(
        "flake8", ".", "--count", "--exit-zero", "--max-complexity=10", "--statistics"
    )  # max-line-length is now in pyproject.toml


@session(venv_backend="uv")
def docs(sess):
    sess.install(".", *proj["project"]["optional-dependencies"]["dev"])
    sess.run("sphinx-build", "docs/source", "docs/build/html")


@session(venv_backend="uv")
def doctest(sess):
    sess.install(".", *proj["project"]["optional-dependencies"]["dev"])
    sess.run("sphinx-build", "-b", "doctest", "docs/source", "docs/build/doctest")
