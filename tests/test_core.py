"""Tests for the core functionality of EnvProfile."""

import json
import tempfile
from pathlib import Path
import unittest

from envprofile.core import ProfileManager


class TestProfileManager(unittest.TestCase):
    """Test suite for the ProfileManager class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        self.manager = ProfileManager(self.config_dir)

    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()

    def test_ensure_config_exists(self):
        """Test that ensure_config_exists creates the config directory and file."""
        # Config directory and file should have been created in setUp
        self.assertTrue(self.config_dir.exists())
        self.assertTrue(self.manager.config_file.exists())

        # File should contain an empty JSON object
        with open(self.manager.config_file, "r") as f:
            content = json.load(f)
            self.assertEqual(content, {})

    def test_create_profile(self):
        """Test creating a new profile."""
        # Create a new profile
        result = self.manager.create_profile("test")
        self.assertTrue(result)

        # Profile should exist in the profiles file
        with open(self.manager.config_file, "r") as f:
            content = json.load(f)
            self.assertIn("test", content)
            self.assertEqual(content["test"], {})

        # Creating the same profile again should return False
        result = self.manager.create_profile("test")
        self.assertFalse(result)

    def test_add_variable(self):
        """Test adding a variable to a profile."""
        # Create a profile
        self.manager.create_profile("test")

        # Add a variable
        result = self.manager.add_variable("test", "KEY", "value")
        self.assertTrue(result)

        # Variable should exist in the profile
        with open(self.manager.config_file, "r") as f:
            content = json.load(f)
            self.assertEqual(content["test"]["KEY"], "value")

        # Adding to non-existent profile should return False
        result = self.manager.add_variable("nonexistent", "KEY", "value")
        self.assertFalse(result)

    def test_remove_variable(self):
        """Test removing a variable from a profile."""
        # Create a profile and add a variable
        self.manager.create_profile("test")
        self.manager.add_variable("test", "KEY", "value")

        # Remove the variable
        result = self.manager.remove_variable("test", "KEY")
        self.assertTrue(result)

        # Variable should no longer exist in the profile
        with open(self.manager.config_file, "r") as f:
            content = json.load(f)
            self.assertNotIn("KEY", content["test"])

        # Removing from non-existent profile should return False
        result = self.manager.remove_variable("nonexistent", "KEY")
        self.assertFalse(result)

        # Removing non-existent key should return False
        result = self.manager.remove_variable("test", "NONEXISTENT")
        self.assertFalse(result)

    def test_get_profile(self):
        """Test getting a profile."""
        # Create a profile and add variables
        self.manager.create_profile("test")
        self.manager.add_variable("test", "KEY1", "value1")
        self.manager.add_variable("test", "KEY2", "value2")

        # Get the profile
        profile = self.manager.get_profile("test")
        self.assertEqual(profile, {"KEY1": "value1", "KEY2": "value2"})

        # Getting non-existent profile should return None
        profile = self.manager.get_profile("nonexistent")
        self.assertIsNone(profile)

    def test_list_profiles(self):
        """Test listing profiles."""
        # Create several profiles with variables
        self.manager.create_profile("test1")
        self.manager.add_variable("test1", "KEY1", "value1")

        self.manager.create_profile("test2")
        self.manager.add_variable("test2", "KEY1", "value1")
        self.manager.add_variable("test2", "KEY2", "value2")

        self.manager.create_profile("empty")

        # List profiles
        profiles = self.manager.list_profiles()
        self.assertEqual(profiles, {"test1": 1, "test2": 2, "empty": 0})

    def test_delete_profile(self):
        """Test deleting a profile."""
        # Create a profile
        self.manager.create_profile("test")

        # Delete the profile
        result = self.manager.delete_profile("test")
        self.assertTrue(result)

        # Profile should no longer exist
        with open(self.manager.config_file, "r") as f:
            content = json.load(f)
            self.assertNotIn("test", content)

        # Deleting non-existent profile should return False
        result = self.manager.delete_profile("nonexistent")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
