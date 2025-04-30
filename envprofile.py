#!/usr/bin/env python3
"""
envprofile - A tool to manage and load environment variable profiles

Usage:
    envprofile create <profile_name>          - Create a new profile
    envprofile add <profile_name> <key> <value> - Add/update an environment variable to a profile
    envprofile remove <profile_name> <key>    - Remove an environment variable from a profile
    envprofile list                           - List all available profiles
    envprofile show <profile_name>            - Show details of a specific profile
    envprofile load <profile_name>            - Load environment variables from a profile
    envprofile delete <profile_name>          - Delete a profile
    envprofile help                           - Show this help message

When using 'load', you need to source the output for it to affect your current shell:
    eval $(envprofile load dev)
"""

import os
import sys
import json
import argparse
from pathlib import Path

CONFIG_DIR = Path.home() / '.config' / 'envprofile'
CONFIG_FILE = CONFIG_DIR / 'profiles.json'

def ensure_config_exists():
    """Ensure the config directory and file exist"""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f, indent=2)

def load_profiles():
    """Load profiles from the config file"""
    ensure_config_exists()
    with open(CONFIG_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_profiles(profiles):
    """Save profiles to the config file"""
    ensure_config_exists()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

def create_profile(args):
    """Create a new profile"""
    profiles = load_profiles()
    if args.profile_name in profiles:
        print(f"Profile '{args.profile_name}' already exists")
        return
    
    profiles[args.profile_name] = {}
    save_profiles(profiles)
    print(f"Created profile '{args.profile_name}'")

def add_variable(args):
    """Add or update an environment variable to a profile"""
    profiles = load_profiles()
    if args.profile_name not in profiles:
        print(f"Profile '{args.profile_name}' does not exist")
        return
    
    profiles[args.profile_name][args.key] = args.value
    save_profiles(profiles)
    print(f"Added/updated '{args.key}={args.value}' to profile '{args.profile_name}'")

def remove_variable(args):
    """Remove an environment variable from a profile"""
    profiles = load_profiles()
    if args.profile_name not in profiles:
        print(f"Profile '{args.profile_name}' does not exist")
        return
    
    if args.key not in profiles[args.profile_name]:
        print(f"Key '{args.key}' does not exist in profile '{args.profile_name}'")
        return
    
    del profiles[args.profile_name][args.key]
    save_profiles(profiles)
    print(f"Removed '{args.key}' from profile '{args.profile_name}'")

def list_profiles(args):
    """List all available profiles"""
    profiles = load_profiles()
    if not profiles:
        print("No profiles available")
        return
    
    print("Available profiles:")
    for profile in profiles:
        var_count = len(profiles[profile])
        print(f"  - {profile} ({var_count} variable{'s' if var_count != 1 else ''})")

def show_profile(args):
    """Show details of a specific profile"""
    profiles = load_profiles()
    if args.profile_name not in profiles:
        print(f"Profile '{args.profile_name}' does not exist")
        return
    
    profile = profiles[args.profile_name]
    if not profile:
        print(f"Profile '{args.profile_name}' is empty")
        return
    
    print(f"Profile: {args.profile_name}")
    print("Environment variables:")
    for key, value in profile.items():
        print(f"  {key}={value}")

def load_profile(args):
    """Load environment variables from a profile
    
    This outputs shell commands that need to be evaluated in the current shell.
    Usage: eval $(envprofile load profile_name)
    """
    profiles = load_profiles()
    if args.profile_name not in profiles:
        print(f"# Profile '{args.profile_name}' does not exist", file=sys.stderr)
        return
    
    profile = profiles[args.profile_name]
    if not profile:
        print(f"# Profile '{args.profile_name}' is empty", file=sys.stderr)
        return
    
    # Generate shell export commands
    for key, value in profile.items():
        # Properly escape the value for shell
        escaped_value = value.replace("'", "'\\''")
        print(f"export {key}='{escaped_value}';")

def delete_profile(args):
    """Delete a profile"""
    profiles = load_profiles()
    if args.profile_name not in profiles:
        print(f"Profile '{args.profile_name}' does not exist")
        return
    
    del profiles[args.profile_name]
    save_profiles(profiles)
    print(f"Deleted profile '{args.profile_name}'")

def main():
    parser = argparse.ArgumentParser(description='Manage environment variable profiles')
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Create profile
    create_parser = subparsers.add_parser('create', help='Create a new profile')
    create_parser.add_argument('profile_name', help='Name of the profile')
    create_parser.set_defaults(func=create_profile)
    
    # Add variable
    add_parser = subparsers.add_parser('add', help='Add/update an environment variable to a profile')
    add_parser.add_argument('profile_name', help='Name of the profile')
    add_parser.add_argument('key', help='Environment variable name')
    add_parser.add_argument('value', help='Environment variable value')
    add_parser.set_defaults(func=add_variable)
    
    # Remove variable
    remove_parser = subparsers.add_parser('remove', help='Remove an environment variable from a profile')
    remove_parser.add_argument('profile_name', help='Name of the profile')
    remove_parser.add_argument('key', help='Environment variable name')
    remove_parser.set_defaults(func=remove_variable)
    
    # List profiles
    list_parser = subparsers.add_parser('list', help='List all available profiles')
    list_parser.set_defaults(func=list_profiles)
    
    # Show profile
    show_parser = subparsers.add_parser('show', help='Show details of a specific profile')
    show_parser.add_argument('profile_name', help='Name of the profile')
    show_parser.set_defaults(func=show_profile)
    
    # Load profile
    load_parser = subparsers.add_parser('load', help='Load environment variables from a profile')
    load_parser.add_argument('profile_name', help='Name of the profile')
    load_parser.set_defaults(func=load_profile)
    
    # Delete profile
    delete_parser = subparsers.add_parser('delete', help='Delete a profile')
    delete_parser.add_argument('profile_name', help='Name of the profile')
    delete_parser.set_defaults(func=delete_profile)
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        print(__doc__)
        return
    
    args.func(args)

if __name__ == '__main__':
    main()