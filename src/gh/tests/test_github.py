from gh import Github

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from nose.tools import eq_, ok_
import requests

def api_down():
    req = requests.get("https://status.github.com/api/status.json")
    status = req.json()

    if status['status'] != "good":
        return True

    return False

API_BAD = api_down()

class TestGithub(unittest.TestCase):

    def test_pass_custom_url_for_ghe(self):
        gh = Github("google.com")

        assert gh.host == "google.com"
        assert gh._is_ghe

    def test_using_github_proper(self):
        gh = Github()

        assert gh.host == "github.com"
        assert gh._is_ghe == False

    @unittest.skipIf(API_BAD, "Github API Down")
    def test_can_get_status_of_service(self):
        gh = Github()
        status, reason = gh.status

        assert status
        assert reason == "All is well"

    def test_status_returns_false_when_service_doesnt_exist(self):
        gh = Github("google.com")
        status, reason = gh.status

        ok_(not status)
        eq_(reason, "No JSON")

    def test_creating_an_api_endpoint_url(self):
        gh = Github()

        eq_(gh._construct_url("issues"), "https://api.github.com/issues")

    def test_endpoint_url_deals_with_blank(self):
        gh = Github()

        eq_(gh._construct_url(""), "https://api.github.com/")

    def test_can_pass_args_to_endpoint_url(self):
        gh =Github()

        eq_(gh._construct_url("users/{user}", user="nZac"),
                "https://api.github.com/users/nZac")

    def test_endpoint_strips_proper_slashes(self):
        gh = Github()

        eq_(gh._construct_url("/users/{user}", user="nZac"),
                "https://api.github.com/users/nZac")
        eq_(gh._construct_url("users/{user}/", user="nZac"),
                "https://api.github.com/users/nZac")
        eq_(gh._construct_url("/users/{user}/", user="nZac"),
                "https://api.github.com/users/nZac")
