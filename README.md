# EnvProfile - Environment Variable Profile Manager

This tool lets you create and manage different sets of environment variables that you can easily load when needed.

## Installation

1. Save the script to a location in your PATH (e.g., `/usr/local/bin/envprofile` or `~/bin/envprofile`):

   ```bash
   # Download the script
   curl -o /usr/local/bin/envprofile https://your-host/path/to/envprofile.py
   
   # Or manually create the file and paste the code in it
   
   # Make it executable
   chmod +x /usr/local/bin/envprofile
   
   # Make sure /usr/local/bin is in your PATH (add to your .bashrc or .zshrc if needed)
   export PATH="/usr/local/bin:$PATH"
   ```

2. Add a shell function to your `.bashrc`, `.zshrc`, or equivalent shell configuration file:

   ```bash
   # Add this to your shell configuration file
   function use-env() {
       eval "$(envprofile load $1)"
   }
   ```

3. Reload your shell configuration:

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
