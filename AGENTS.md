## Build/Test/Lint Commands

### Testing

- Run all tests: `uv run nox -s tests`
- Run tests for specific Python version: `uv run nox -s tests-3.10`
- Run pytest directly with coverage: `uv run pytest --cov=secretsanta --cov-report term-missing`
- Run a single test file: `uv run pytest tests/main/test_core.py`
- Run a specific test: `uv run pytest tests/main/test_core.py::TestSecretSanta::test_secret_santa_init___result_has_helper_rudolph`
- Run single test via nox: `uv run nox -s tests -- tests/main/test_core.py::TestSecretSanta::test_secret_santa_init___result_has_helper_rudolph`

### Linting & Formatting

- Full lint: `uv run nox -s lint`
- Lint directly: `uv run ruff check`
- Check formatting: `uv run ruff format --check`
- Auto-format: `uv run ruff format`

### Type Checking

- Run typecheck via nox: `uv run nox -s typecheck`
- Run mypy directly: `uv run mypy .`
- Run mypy on specific file: `uv run mypy ./secretsanta/main/core.py`

### Documentation

- Build docs: `uv run nox -s docs`
- Run doctests: `uv run nox -s doctest`

## Code Style Guidelines

### Imports

Order: standard library → third-party → local modules, separated by blank lines.

### Type Hints

- Use Python 3.9+ syntax: `list[str]`, `dict[str, str]`
- Forward references with string quotes: `"SecretSanta"`
- Prefer `int | None` over `Optional[int]`
- Always annotate function arguments and return values
- Use mypy in strict mode

### Naming Conventions

- Classes: `PascalCase` (e.g., `SecretSanta`)
- Functions/variables: `snake_case` (e.g., `make_santa_dict`)
- Protected attributes: leading underscore (e.g., `_helper`)
- Private methods: double underscore (rare)

### Error Handling

- Use `contextlib.suppress(ValueError)` to ignore known exceptions
- Log errors via `logger.error()` and raise descriptive exceptions
- Raise `ValueError` for invalid input

### Logging

- Set up logging with `setup_logging(level)` from utils
- Get logger: `logger = logging.getLogger(__name__)`
- Log levels: `error`, `warning`, `info` based on severity
- Log files auto-created in `./log_files/` directory

### Docstrings

- Google style docstrings
- Include Args, Returns, and where applicable Example sections
- Docstring examples serve as doctests

### Testing

- Use `unittest.TestCase` for unit tests
- Mock external dependencies with `unittest.mock.patch`
- Property testing with Hypothesis `@given` decorator
- Test files in `tests/` mirroring `secretsanta/` structure
- Use custom mock validators for complex assertions

### CLI

- Use Click decorators for command definition
- Group commands under main group: `@click.group()`
- Provide help strings for all arguments/options

### General

- Line length: 127 characters (matches GitHub editor width)
- Ruff handles all linting/formatting rules
- Avoid inline comments
- Use property decorators for getter-only access
- Prefer dictionary comprehensions for transformations
