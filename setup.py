#!/usr/bin/env python3
"""Setup script for EnvProfile package."""

from setuptools import setup, find_packages
import os

# Read version from package __init__.py
with open(os.path.join("src", "envprofile", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

# Read long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="envprofile",
    version=version,
    description="Environment Variable Profile Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="EnvProfile Authors",
    author_email="your@email.com",
    url="https://github.com/yourusername/envprofile",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "envprofile=envprofile.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.1.0",
            "flake8>=5.0.0",
            "mypy>=0.950",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
) 