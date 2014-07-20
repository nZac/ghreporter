import requests


class Github(object):

    # a flag for telling if the is an enterprise version of Github
    _is_ghe = False

    # github host url, used for Github Enterprise installations
    host = "github.com"


    def __init__(self, host=None):

        if host is not None:
            self._is_ghe = True
            self.host = host

    @property
    def status(self):
        """Returns the up/down status of the API with a message"""

        if self._is_ghe:
            url = self._construct_url("")
        else:
            url = "https://status.github.com/api/status.json"

        req = requests.get(url)

        try:
            status = req.json()
        except ValueError:
            return (False, "No JSON")

        if req.status_code != 200:
            return (False, "Not 200")

        if not self._is_ghe and status['status'] != "good":
            return (False, "API Down")

        if self._is_ghe and "X-GitHub-Request-Id" not in req.headers:
            return (False, "Bad GHE Server")

        if not self._is_ghe and "x-octostatus-request-id" not in req.headers:
            return (False, "Bad Github Server")

        return (True, "All is well")

    def _construct_url(self, endpoint, **kwargs):

        endpoint = endpoint.lstrip("/").rstrip("/")

        if self._is_ghe:
            url_format = "https://{host}/api/v3/" + endpoint
        else:
            url_format = "https://api.{host}/" + endpoint

        return url_format.format(host=self.host, endpoint=endpoint, **kwargs)

