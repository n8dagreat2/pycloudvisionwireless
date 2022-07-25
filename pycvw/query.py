try:
    import concurrent.futures as cf
except ImportError:
    pass
import json


class RequestError(Exception):
    def __init__(self, message):
        req = message

        if req.status_code == 404:
            message = "The requested url: {} could not be found.".format(req.url)
        elif req.status_code == 401:
            message = "An authentication error occured. Try signing back in before continuing."
        else:
            try:
                message = "The request failed with code {} {}: {}".format(
                    req.status_code, req.reason, req.json()
                )
            except ValueError:
                message = (
                    "The request failed with code {} {} but more specific "
                    "details were not returned in json. Check the CloudVision Logs "
                    "or investigate this exception's error attribute.".format(
                        req.status_code, req.reason
                    )
                )
        super(RequestError, self).__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = req.text


class ContentError(Exception):
    def __init__(self, message):
        req = message

        message = "The server returned invalid (non-json) data. Possibly passed invalid functions?"
        super(ContentError, self).__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.base = req.url
        self.error = message


class Request(object):
    def __init__(
        self,
        base: str,
        http_session,
        key: str = None,
        token: dict = None,
        filters=None,
        threading: bool = False,
        api_version: str = None,
    ):
        self.base = self.normalize_url(base)
        self.filters = filters
        self.key = key
        self.token = token
        self.http_session = http_session
        self.threading = threading
        self.api_version = api_version

    def normalize_url(self, url):
        if url[-1] == "/":
            return url[:-1]
        return url
