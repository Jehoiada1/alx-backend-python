#!/usr/bin/env python3
"""Test client.GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc", "repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test org method"""
        # Set up mock
        mock_get_json.return_value = expected_response
        
        # Test client
        client = GithubOrgClient(org_name)
        
        # First call - should call get_json
        result = client.org()
        self.assertEqual(result, expected_response)
        
        # Second call - should return cached result
        result = client.org()
        self.assertEqual(result, expected_response)
        
        # Verify get_json was called exactly once
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        
        # Patch the org method (not property)
        with patch.object(
            GithubOrgClient, 
            'org',
            return_value=test_payload
        ):
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        test_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_repos
        
        # Patch both the URL property and repos_payload method
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ), patch.object(
            GithubOrgClient,
            'repos_payload',
            return_value=test_repos
        ):
            client = GithubOrgClient("test")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )
