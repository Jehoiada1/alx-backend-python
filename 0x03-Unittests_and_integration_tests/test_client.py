#!/usr/bin/env python3
"""Test client.GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Setup mock return value
        expected_response = {"login": org_name, "id": 123456}
        mock_get_json.return_value = expected_response

        # Create client instance and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        
        # Assert the result matches expected response
        self.assertEqual(result, expected_response)
