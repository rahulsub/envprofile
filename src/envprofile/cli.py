"""
Command-line interface for EnvProfile.

This module provides the command-line interface for interacting with the EnvProfile tool.
"""

import sys
import argparse
from typing import List, Optional

from .core import ProfileManager


def create_profile_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Create a new profile command handler."""
    if manager.create_profile(args.profile_name):
        print(f"Created profile '{args.profile_name}'")
        return 0
    else:
        print(f"Profile '{args.profile_name}' already exists")
        return 1


def add_variable_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Add a variable to a profile command handler."""
    if manager.add_variable(args.profile_name, args.key, args.value):
        msg = (
            f"Added/updated '{args.key}={args.value}' to profile '{args.profile_name}'"
        )
        print(msg)
        return 0
    else:
        print(f"Profile '{args.profile_name}' does not exist")
        return 1


def remove_variable_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Remove a variable from a profile command handler."""
    result = manager.remove_variable(args.profile_name, args.key)
    if not result:
        profiles = manager.load_profiles()
        if args.profile_name not in profiles:
            print(f"Profile '{args.profile_name}' does not exist")
        else:
            key = args.key
            profile = args.profile_name
            print(f"Key '{key}' does not exist in profile '{profile}'")
        return 1

    print(f"Removed '{args.key}' from profile '{args.profile_name}'")
    return 0


def list_profiles_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """List all profiles command handler."""
    profiles = manager.list_profiles()
    if not profiles:
        print("No profiles available")
        return 0

    print("Available profiles:")
    for profile, var_count in profiles.items():
        suffix = "s" if var_count != 1 else ""
        print(f"  - {profile} ({var_count} variable{suffix})")

    return 0


def show_profile_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Show a profile's details command handler."""
    profile = manager.get_profile(args.profile_name)
    if profile is None:
        print(f"Profile '{args.profile_name}' does not exist")
        return 1

    if not profile:
        print(f"Profile '{args.profile_name}' is empty")
        return 0

    print(f"Profile: {args.profile_name}")
    print("Environment variables:")
    for key, value in profile.items():
        print(f"  {key}={value}")

    return 0


def load_profile_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Load a profile's environment variables command handler."""
    profile = manager.get_profile(args.profile_name)
    if profile is None:
        msg = f"# Profile '{args.profile_name}' does not exist"
        print(msg, file=sys.stderr)
        return 1

    if not profile:
        print(f"# Profile '{args.profile_name}' is empty", file=sys.stderr)
        return 0

    # Generate shell export commands
    for key, value in profile.items():
        # Properly escape the value for shell
        escaped_value = value.replace("'", "'\\''")
        print(f"export {key}='{escaped_value}';")

    return 0


def delete_profile_cmd(manager: ProfileManager, args: argparse.Namespace) -> int:
    """Delete a profile command handler."""
    if manager.delete_profile(args.profile_name):
        print(f"Deleted profile '{args.profile_name}'")
        return 0
    else:
        print(f"Profile '{args.profile_name}' does not exist")
        return 1


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Manage environment variable profiles",
        epilog="""
When using 'load', you need to source the output for it to affect your current shell:
    eval $(envprofile load dev)

Or use the provided shell function:
    use-env dev
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Create profile
    create_parser = subparsers.add_parser("create", help="Create a new profile")
    create_parser.add_argument("profile_name", help="Name of the profile")

    # Add variable
    add_parser = subparsers.add_parser(
        "add", help="Add/update an environment variable to a profile"
    )
    add_parser.add_argument("profile_name", help="Name of the profile")
    add_parser.add_argument("key", help="Environment variable name")
    add_parser.add_argument("value", help="Environment variable value")

    # Remove variable
    remove_parser = subparsers.add_parser(
        "remove", help="Remove an environment variable from a profile"
    )
    remove_parser.add_argument("profile_name", help="Name of the profile")
    remove_parser.add_argument("key", help="Environment variable name")

    # List profiles
    subparsers.add_parser("list", help="List all available profiles")

    # Show profile
    show_parser = subparsers.add_parser(
        "show", help="Show details of a specific profile"
    )
    show_parser.add_argument("profile_name", help="Name of the profile")

    # Load profile
    load_parser = subparsers.add_parser(
        "load", help="Load environment variables from a profile"
    )
    load_parser.add_argument("profile_name", help="Name of the profile")

    # Delete profile
    delete_parser = subparsers.add_parser("delete", help="Delete a profile")
    delete_parser.add_argument("profile_name", help="Name of the profile")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        args: Command line arguments (if None, sys.argv[1:] is used)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = get_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    manager = ProfileManager()

    # Command -> function mapping
    commands = {
        "create": create_profile_cmd,
        "add": add_variable_cmd,
        "remove": remove_variable_cmd,
        "list": list_profiles_cmd,
        "show": show_profile_cmd,
        "load": load_profile_cmd,
        "delete": delete_profile_cmd,
    }

    # Execute the corresponding function
    return commands[parsed_args.command](manager, parsed_args)


if __name__ == "__main__":
    sys.exit(main())
