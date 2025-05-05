"""Integration tests for the EnvProfile package."""

import os
import json
import tempfile
import unittest
import subprocess
from pathlib import Path
import sys


class TestIntegration(unittest.TestCase):
    """Integration test suite for EnvProfile."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / ".config" / "envprofile"
        self.config_dir.mkdir(parents=True)
        self.config_file = self.config_dir / "profiles.json"

        # Create an empty profiles file
        with open(self.config_file, "w") as f:
            json.dump({}, f)

        # Set environment variable to point to our test config
        self.original_home = os.environ.get("HOME")
        os.environ["HOME"] = str(self.temp_dir.name)

        # Path to the module
        self.module_path = "envprofile.cli"

    def tearDown(self):
        """Tear down test fixtures."""
        # Restore original HOME environment variable
        if self.original_home:
            os.environ["HOME"] = self.original_home
        else:
            del os.environ["HOME"]

        self.temp_dir.cleanup()

    def run_command(self, args):
        """Run a command using the CLI module and return the output and exit code."""
        cmd = [sys.executable, "-m", self.module_path] + args
        process = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
        )
        return process.stdout, process.stderr, process.returncode

    def test_full_workflow(self):
        """Test a full workflow of creating, adding, listing, and loading profiles."""
        # Create a profile
        stdout, stderr, exit_code = self.run_command(["create", "dev"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Created profile 'dev'", stdout)

        # Add some variables
        cmd = ["add", "dev", "DB_HOST", "localhost"]
        stdout, stderr, exit_code = self.run_command(cmd)
        self.assertEqual(exit_code, 0)

        expected = "Added/updated 'DB_HOST=localhost' to profile 'dev'"
        self.assertIn(expected, stdout)

        stdout, stderr, exit_code = self.run_command(["add", "dev", "DB_PORT", "5432"])
        self.assertEqual(exit_code, 0)

        # List profiles
        stdout, stderr, exit_code = self.run_command(["list"])
        self.assertEqual(exit_code, 0)
        self.assertIn("dev (2 variables)", stdout)

        # Show profile
        stdout, stderr, exit_code = self.run_command(["show", "dev"])
        self.assertEqual(exit_code, 0)
        self.assertIn("DB_HOST=localhost", stdout)
        self.assertIn("DB_PORT=5432", stdout)

        # Load profile
        stdout, stderr, exit_code = self.run_command(["load", "dev"])
        self.assertEqual(exit_code, 0)

        # Check output for environment variables
        self.assertIn("export DB_HOST='localhost';", stdout)
        self.assertIn("export DB_PORT='5432';", stdout)

        # Remove a variable
        cmd = ["remove", "dev", "DB_PORT"]
        stdout, stderr, exit_code = self.run_command(cmd)
        self.assertEqual(exit_code, 0)
        self.assertIn("Removed 'DB_PORT' from profile 'dev'", stdout)

        # Show profile again to verify removal
        stdout, stderr, exit_code = self.run_command(["show", "dev"])
        self.assertEqual(exit_code, 0)
        self.assertIn("DB_HOST=localhost", stdout)
        self.assertNotIn("DB_PORT=5432", stdout)

        # Delete profile
        stdout, stderr, exit_code = self.run_command(["delete", "dev"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Deleted profile 'dev'", stdout)

        # List profiles to verify deletion
        stdout, stderr, exit_code = self.run_command(["list"])
        self.assertEqual(exit_code, 0)
        self.assertIn("No profiles available", stdout)

    def test_error_handling(self):
        """Test error handling for various scenarios."""
        # Try to show a non-existent profile
        profile_cmd = ["show", "nonexistent"]
        stdout, stderr, exit_code = self.run_command(profile_cmd)
        self.assertEqual(exit_code, 1)
        self.assertIn("does not exist", stdout)

        # Try to add a variable to a non-existent profile
        cmd = ["add", "nonexistent", "KEY", "value"]
        stdout, stderr, exit_code = self.run_command(cmd)
        self.assertEqual(exit_code, 1)
        self.assertIn("does not exist", stdout)

        # Try to remove a variable from a non-existent profile
        cmd = ["remove", "nonexistent", "KEY"]
        stdout, stderr, exit_code = self.run_command(cmd)
        self.assertEqual(exit_code, 1)
        self.assertIn("does not exist", stdout)

        # Try to delete a non-existent profile
        cmd = ["delete", "nonexistent"]
        stdout, stderr, exit_code = self.run_command(cmd)
        self.assertEqual(exit_code, 1)
        self.assertIn("does not exist", stdout)


if __name__ == "__main__":
    unittest.main()
