# Contributing to EnvProfile

Thank you for your interest in contributing to EnvProfile! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when participating in this project.

## Getting Started

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/envprofile.git
   cd envprofile
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   pip install -r requirements.txt
   ```

3. Run the tests to verify your setup:
   ```bash
   pytest
   ```

## Development Workflow

### Branching Strategy

- Use `main` branch for stable releases
- Create feature branches from `main` named with the pattern: `feature/your-feature-name`
- Create bug fix branches with the pattern: `bugfix/issue-description`

### Making Changes

1. Create a new branch for your changes
2. Make your changes with clear, descriptive commit messages
3. Add tests for your changes
4. Run tests and ensure all pass
5. Update documentation if necessary
6. Submit a pull request

### Code Style

We follow PEP 8 guidelines for Python code. Use the following tools to ensure your code conforms to our style:

- **Black**: For code formatting
  ```bash
  black src tests
  ```

- **Flake8**: For style guide enforcement
  ```bash
  flake8 src tests
  ```

- **MyPy**: For type checking
  ```bash
  mypy src
  ```

### Testing

All changes should include tests. Run the test suite with:

```bash
pytest
```

To see test coverage information:

```bash
pytest --cov=envprofile
```

## Pull Request Process

1. Ensure all tests pass and code style checks pass
2. Update the README.md or documentation with details of changes if applicable
3. The PR should work for Python 3.6 and later versions
4. Include a clear and descriptive PR title and description
5. Link any related issues in the PR description

## Release Process

Releases are handled by the project maintainers. The process typically involves:

1. Updating the version in `src/envprofile/__init__.py`
2. Updating the changelog
3. Creating a tagged release

## Documentation

- Update the README.md file for user-focused documentation
- Add docstrings for all public modules, functions, classes, and methods
- Use clear and descriptive variable names and comments

## Bug Reports and Feature Requests

Please use the GitHub issue tracker to report bugs or request features. When reporting bugs:

1. Check if the bug has already been reported
2. Use a clear and descriptive title
3. Provide detailed steps to reproduce the bug
4. Include expected and actual behavior
5. Provide your environment details (OS, Python version, etc.)

## Contact

If you have questions about contributing, please open an issue on GitHub or contact the maintainers directly. 