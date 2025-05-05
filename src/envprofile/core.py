"""
Core functionality for the EnvProfile package.

This module handles the loading, saving, and manipulation of environment profiles.
"""

import json
from pathlib import Path
from typing import Dict, Optional


class ProfileManager:
    """Manages environment variable profiles."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the profile manager.

        Args:
            config_dir: Optional directory path for configuration files.
                        If None, defaults to ~/.config/envprofile
        """
        if config_dir is None:
            self.config_dir = Path.home() / ".config" / "envprofile"
        else:
            self.config_dir = config_dir

        self.config_file = self.config_dir / "profiles.json"
        self.ensure_config_exists()

    def ensure_config_exists(self) -> None:
        """Ensure the config directory and file exist."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)

        if not self.config_file.exists():
            with open(self.config_file, "w") as f:
                json.dump({}, f, indent=2)

    def load_profiles(self) -> Dict[str, Dict[str, str]]:
        """
        Load profiles from the config file.

        Returns:
            Dict mapping profile names to their environment variables
        """
        self.ensure_config_exists()
        with open(self.config_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_profiles(self, profiles: Dict[str, Dict[str, str]]) -> None:
        """
        Save profiles to the config file.

        Args:
            profiles: Dict mapping profile names to their environment variables
        """
        self.ensure_config_exists()
        with open(self.config_file, "w") as f:
            json.dump(profiles, f, indent=2)

    def create_profile(self, profile_name: str) -> bool:
        """
        Create a new profile.

        Args:
            profile_name: Name of the profile to create

        Returns:
            True if profile was created, False if it already exists
        """
        profiles = self.load_profiles()
        if profile_name in profiles:
            return False

        profiles[profile_name] = {}
        self.save_profiles(profiles)
        return True

    def add_variable(self, profile_name: str, key: str, value: str) -> bool:
        """
        Add or update an environment variable to a profile.

        Args:
            profile_name: Name of the profile
            key: Environment variable name
            value: Environment variable value

        Returns:
            True if successful, False if profile doesn't exist
        """
        profiles = self.load_profiles()
        if profile_name not in profiles:
            return False

        profiles[profile_name][key] = value
        self.save_profiles(profiles)
        return True

    def remove_variable(self, profile_name: str, key: str) -> bool:
        """
        Remove an environment variable from a profile.

        Args:
            profile_name: Name of the profile
            key: Environment variable name to remove

        Returns:
            True if successful, False if profile or key doesn't exist
        """
        profiles = self.load_profiles()
        if profile_name not in profiles:
            return False

        if key not in profiles[profile_name]:
            return False

        del profiles[profile_name][key]
        self.save_profiles(profiles)
        return True

    def get_profile(self, profile_name: str) -> Optional[Dict[str, str]]:
        """
        Get a specific profile's environment variables.

        Args:
            profile_name: Name of the profile

        Returns:
            Dict of environment variables or None if profile doesn't exist
        """
        profiles = self.load_profiles()
        return profiles.get(profile_name)

    def list_profiles(self) -> Dict[str, int]:
        """
        Get all available profiles with their variable counts.

        Returns:
            Dict mapping profile names to their variable counts
        """
        profiles = self.load_profiles()
        return {name: len(variables) for name, variables in profiles.items()}

    def delete_profile(self, profile_name: str) -> bool:
        """
        Delete a profile.

        Args:
            profile_name: Name of the profile to delete

        Returns:
            True if successful, False if profile doesn't exist
        """
        profiles = self.load_profiles()
        if profile_name not in profiles:
            return False

        del profiles[profile_name]
        self.save_profiles(profiles)
        return True
