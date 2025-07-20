#!/usr/bin/env python3
"""Test client.GithubOrgClient class"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    # Task 4 - Test org method
    @parameterized.expand([
        ("google", {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc", "repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        
        # First call - should call get_json
        self.assertEqual(client.org(), expected_response)
        
        # Second call - should return cached result
        self.assertEqual(client.org(), expected_response)
        
        # Verify get_json was called exactly once
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    # Task 5 - Test _public_repos_url property
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )
            mock_org.assert_called_once()

    # Task 6 - Test public_repos method
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ) as mock_url:
            client = GithubOrgClient("test")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")
            mock_url.assert_called_once()

    # Task 7 - Test has_license method
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
