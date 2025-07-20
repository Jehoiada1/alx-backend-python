#!/usr/bin/env python3
"""Test client.GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "repos_url": "https://example.com/google/repos"}),
        ("abc", {"login": "abc", "repos_url": "https://example.com/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        
        # First call
        result = client.org()
        self.assertEqual(result, expected_response)
        
        # Second call (should be memoized)
        result = client.org()
        self.assertEqual(result, expected_response)
        
        # Should only be called once due to memoization
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        test_payload = {"repos_url": "https://example.com/test/repos"}
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://example.com/test/repos"
            )
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value="https://example.com/test/repos"
        ) as mock_url:
            client = GithubOrgClient("test")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://example.com/test/repos")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )
