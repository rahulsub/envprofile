"""Tests for the CLI functionality of EnvProfile."""

import io
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from envprofile.cli import main


class TestCLI(unittest.TestCase):
    """Test suite for the CLI interface."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)

        # Create a patcher for ProfileManager
        self.patcher = patch("envprofile.cli.ProfileManager")
        self.mock_profile_manager_class = self.patcher.start()

        # Create a mock instance that will be returned by ProfileManager()
        self.mock_manager = MagicMock()
        self.mock_profile_manager_class.return_value = self.mock_manager

    def tearDown(self):
        """Tear down test fixtures."""
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_create_profile(self):
        """Test the create profile command."""
        # Set up the mock to return True (success)
        self.mock_manager.create_profile.return_value = True

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        exit_code = main(["create", "test"])

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check that the correct method was called
        self.mock_manager.create_profile.assert_called_once_with("test")

        # Check the output
        self.assertIn("Created profile 'test'", captured_output.getvalue())

        # Check the exit code
        self.assertEqual(exit_code, 0)

        # Now test the failure case
        self.mock_manager.create_profile.return_value = False

        captured_output = io.StringIO()
        sys.stdout = captured_output

        exit_code = main(["create", "test"])

        sys.stdout = sys.__stdout__

        self.assertIn("already exists", captured_output.getvalue())
        self.assertEqual(exit_code, 1)

    def test_add_variable(self):
        """Test the add variable command."""
        # Set up the mock to return True (success)
        self.mock_manager.add_variable.return_value = True

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        exit_code = main(["add", "test", "KEY", "value"])

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check that the correct method was called
        self.mock_manager.add_variable.assert_called_once_with("test", "KEY", "value")

        # Check the output
        self.assertIn(
            "Added/updated 'KEY=value' to profile 'test'", captured_output.getvalue()
        )

        # Check the exit code
        self.assertEqual(exit_code, 0)

        # Now test the failure case
        self.mock_manager.add_variable.return_value = False

        captured_output = io.StringIO()
        sys.stdout = captured_output

        exit_code = main(["add", "test", "KEY", "value"])

        sys.stdout = sys.__stdout__

        self.assertIn("does not exist", captured_output.getvalue())
        self.assertEqual(exit_code, 1)

    def test_list_profiles(self):
        """Test the list profiles command."""
        # Set up the mock to return a dict of profiles
        self.mock_manager.list_profiles.return_value = {"test1": 1, "test2": 2}

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        exit_code = main(["list"])

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check that the correct method was called
        self.mock_manager.list_profiles.assert_called_once()

        # Check the output
        output = captured_output.getvalue()
        self.assertIn("Available profiles:", output)
        self.assertIn("test1 (1 variable)", output)
        self.assertIn("test2 (2 variables)", output)

        # Check the exit code
        self.assertEqual(exit_code, 0)

        # Now test the empty case
        self.mock_manager.list_profiles.return_value = {}

        captured_output = io.StringIO()
        sys.stdout = captured_output

        exit_code = main(["list"])

        sys.stdout = sys.__stdout__

        self.assertIn("No profiles available", captured_output.getvalue())
        self.assertEqual(exit_code, 0)

    def test_load_profile(self):
        """Test the load profile command."""
        # Set up the mock to return a profile
        self.mock_manager.get_profile.return_value = {
            "KEY1": "value1",
            "KEY2": "value with spaces",
        }

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the function
        exit_code = main(["load", "test"])

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check that the correct method was called
        self.mock_manager.get_profile.assert_called_once_with("test")

        # Check the output
        output = captured_output.getvalue()
        # Split assertions to avoid long lines
        self.assertIn("export KEY1='value1';", output)
        self.assertIn("export KEY2='value with spaces';", output)

        # Check the exit code
        self.assertEqual(exit_code, 0)

        # Now test when profile doesn't exist
        self.mock_manager.get_profile.return_value = None

        # Capture stderr
        captured_error = io.StringIO()
        sys.stderr = captured_error

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        exit_code = main(["load", "test"])

        # Reset stderr and stdout
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

        self.assertIn("does not exist", captured_error.getvalue())
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
