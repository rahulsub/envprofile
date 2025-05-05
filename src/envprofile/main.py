#!/usr/bin/env python3
"""
Main executable script for EnvProfile.

This is the main entry point for direct execution as a script.
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
