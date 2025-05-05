# EnvProfile - Environment Variable Profile Manager

[![Python Tests](https://github.com/yourusername/envprofile/actions/workflows/python-tests.yml/badge.svg)](https://github.com/yourusername/envprofile/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/envprofile.svg)](https://badge.fury.io/py/envprofile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EnvProfile is a tool that lets you create and manage different sets of environment variables that you can easily load when needed. This is particularly useful for developers who work with different projects that require different environment configurations.

## Features

- Create multiple named environment profiles
- Add, remove, and update environment variables in profiles
- Load environment variables from profiles into your current shell
- List available profiles and view their contents
- Easy to use command-line interface

## Installation

### From PyPI (Recommended)

```bash
pip install envprofile
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/envprofile.git
cd envprofile

# Install the package
pip install -e .
```

### Shell Integration

Add a shell function to your `.bashrc`, `.zshrc`, or equivalent shell configuration file:

```bash
# Add this to your shell configuration file
function use-env() {
    eval "$(envprofile load $1)"
}
```

Reload your shell configuration:

```bash
source ~/.bashrc  # or ~/.zshrc
```

## Usage Examples

### Creating Profiles

```bash
# Create a new profile for development environment
envprofile create dev

# Add environment variables to the profile
envprofile add dev DB_HOST localhost
envprofile add dev DB_PORT 5432
envprofile add dev API_KEY dev_api_key_123
envprofile add dev DEBUG true

# Create another profile for production
envprofile create prod
envprofile add prod DB_HOST production.example.com
envprofile add prod DB_PORT 5432
envprofile add prod API_KEY prod_api_key_456
envprofile add prod DEBUG false
```

### Managing Profiles

```bash
# List all available profiles
envprofile list

# Show details of a specific profile
envprofile show dev

# Remove a variable from a profile
envprofile remove dev DEBUG

# Delete an entire profile
envprofile delete test
```

### Loading Profiles

```bash
# Method 1: Using the shell function defined during installation
use-env dev

# Method 2: Direct evaluation
eval $(envprofile load prod)
```

### Checking Active Environment Variables

```bash
# After loading a profile, you can verify the environment variables are set
echo $DB_HOST
echo $API_KEY
```

## Configuration

All profiles are stored in a single JSON file at `~/.config/envprofile/profiles.json`. The format is:

```json
{
  "dev": {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "API_KEY": "dev_api_key_123"
  },
  "prod": {
    "DB_HOST": "production.example.com",
    "DB_PORT": "5432",
    "API_KEY": "prod_api_key_456"
  }
}
```

## Advanced Usage

### Using with Docker

You can use EnvProfile to generate environment files for Docker:

```bash
# Generate a .env file for docker-compose
envprofile load dev > .env
```

### Using with Multiple Projects

Create project-specific profiles by using prefixes:

```bash
# Create profiles for different projects
envprofile create project1-dev
envprofile create project1-prod
envprofile create project2-dev
```

## Troubleshooting

### Common Issues

**Issue**: Changes to environment variables not appearing in the shell

**Solution**: Make sure you're using the `eval` command or the `use-env` function as described in the installation section.

**Issue**: Error "command not found: envprofile"

**Solution**: Ensure that the installation directory is in your PATH or install using pip.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by various environment management tools like direnv and autoenv
- Thanks to all contributors
