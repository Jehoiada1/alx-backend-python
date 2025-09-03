#!/usr/bin/env python3
"""Test client.GithubOrgClient class."""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        expected = {
            "google": {
                "login": "google",
                "repos_url": "https://api.github.com/orgs/google/repos"
            },
            "abc": {
                "login": "abc",
                "repos_url": "https://api.github.com/orgs/abc/repos"
            },
        }[org_name]
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == '__main__':
    unittest.main()
