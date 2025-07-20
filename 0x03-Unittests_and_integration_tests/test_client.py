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
    @patch('client.GithubOrgClient._org', new_callable=PropertyMock)
    def test_org(self, org_name, expected_response, mock_org):
        """Test that GithubOrgClient.org returns correct value"""
        # Set the mock return value
        mock_org.return_value = expected_response

        # Create client instance and call org property
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_response)
        mock_org.assert_called_once()
