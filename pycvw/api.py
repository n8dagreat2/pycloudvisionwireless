import requests
import json

from pycloudvisionwireless.pycvw.query import Request, RequestError


class Api(object):
    def __init__(
        self,
        url: str,
        key: str,
        value: str,
        timeout: int = 120,
    ):
        base_url = "{}/wifi/api/".format(url if url[-1] != "/" else url[:-1])
        self.api_key = key
        self.api_value = value
        self._headers = {
            "Content-Type": "application/json",
            "timeout": "{}".format(timeout),
        }
        self.base_url = base_url
        self.http_session = requests.Session()
        self.cookie = self.sign_in(
            self.base_url, self._headers, self.api_key, self.api_value
        )
        self._headers.update({"Cookie": "JSESSIONID={}".format(self.cookie)})
        self.http_session.headers.update(self._headers)

    def sign_in(self, base, header, api_key, api_value):
        url = f"{base}/session"

        payload = json.dumps(
            {
                "type": "apikeycredentials",
                "keyId": f"{api_key}",
                "keyValue": f"{api_value}",
            }
        )
        response = requests.request("POST", url, data=payload, headers=header)
        if response.ok:
            return response.cookies["JSESSIONID"]
        else:
            raise RequestError(response)


cvw = Api(
    url="https://awm13104-c4.srv.wifi.arista.com",
    key="KEY-ATN566147-1155",
    value="a8bac48f1725d22d5f8be4d4e75f7f2e",
)
