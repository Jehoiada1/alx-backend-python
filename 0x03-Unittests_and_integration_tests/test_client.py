#!/usr/bin/env python3
"""Test client.GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "id": 123456}),
        ("abc", {"login": "abc", "id": 789012}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Set up the mock
        mock_get_json.return_value = expected_response

        # Create client instance and call org method
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected_response)

        # Verify get_json was called with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
