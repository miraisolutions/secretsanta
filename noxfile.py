import nox
from nox import session

# load project deps from pyproject.toml
import nox.project
proj = nox.project.load_toml("pyproject.toml")

@session(python=["3.8","3.9","3.10","3.11","3.12"])
def tests(sess):
    # install runtime + dev deps
    sess.install(".", *proj["project"]["optional-dependencies"]["dev"])
    sess.run("pytest", "--cov=secretsanta")

@session
def lint(sess):
    sess.install(".", "flake8")
    sess.run("flake8", "secretsanta", "tests")

@session
def docs(sess):
    sess.install(".", *proj["project"]["optional-dependencies"]["dev"])
    sess.run("sphinx-build", "docs/source", "docs/build/html")