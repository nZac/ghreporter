from gh import Github

import unittest
import requests

def api_down():
    req = requests.get("https://status.github.com/api/status.json")
    status = req.json()

    if status['status'] != "good":
        return True

    return False

API_BAD = api_down()

def test_pass_custom_url():
    gh = Github("something.com")

@unittest.skipIf(API_BAD, "Github API Down")
def test_can_get_test_access_to_remote():
    gh = Github()
    assert gh.status
