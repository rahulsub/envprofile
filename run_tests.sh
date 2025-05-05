#!/bin/bash
# Script to run tests and code quality checks

set -e  # Exit on any error

# Use the Python where we installed our package
PYTHON="python3.9"  # This should match the version we installed the package with

# Run code formatting
echo "Running Black code formatter..."
$PYTHON -m black src tests

# Run linting
echo "Running Flake8 linter..."
$PYTHON -m flake8 src tests --max-line-length=100

# Run type checking
echo "Running MyPy type checker..."
$PYTHON -m mypy src

# Run tests with coverage
echo "Running tests without coverage..."
$PYTHON -m pytest

# Show success message
echo "All tests and checks passed!" 