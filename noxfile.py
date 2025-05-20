import nox
from nox import session

# load project deps from pyproject.toml
import nox.project

proj = nox.project.load_toml("pyproject.toml")


@session(python=["3.9", "3.10", "3.11", "3.12", "3.13"], venv_backend="uv")
def tests(sess):
    # install runtime + dev deps
    sess.install(".", *proj["dependency-groups"]["dev"])
    sess.run("pytest", "--cov=secretsanta")


@session(venv_backend="uv")
def lint(sess):
    sess.install(".", "ruff")
    sess.run("ruff", "check")
    sess.run("ruff", "format", "--check")


@session(venv_backend="uv", default=False)
def lint_critical(sess):
    sess.install(".", "ruff")
    # stop the build if there are Python syntax errors or undefined names
    sess.run(
        "ruff",
        "check",
        ".",
        "--select=E9,F63,F7,F82",
        "--statistics",
    )


@session(venv_backend="uv", default=False)
def lint_style(sess):
    sess.install(".", "ruff")
    sess.run("ruff", "check", "--exit-zero", "--statistics")


@session(venv_backend="uv")
def typecheck(sess):
    sess.install(".", "mypy")
    sess.run("mypy", "--strict", ".")


@session(venv_backend="uv")
def docs(sess):
    sess.install(".", *proj["dependency-groups"]["dev"])
    sess.run("sphinx-build", "docs/source", "docs/build/html")


@session(venv_backend="uv")
def doctest(sess):
    sess.install(".", *proj["dependency-groups"]["dev"])
    sess.run("sphinx-build", "-b", "doctest", "docs/source", "docs/build/doctest")
