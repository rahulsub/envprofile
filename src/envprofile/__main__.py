"""
Main entry point for the EnvProfile package.

This allows the package to be run as a module (python -m envprofile).
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
