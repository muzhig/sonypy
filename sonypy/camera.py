import functools
import json
import requests


class Camera(object):
    def __init__(self, endpoint, version='1.0'):
        self.endpoint = endpoint
        self.version = version
        self.num_requests = 0

    def __getattr__(self, method_name):
        return functools.partial(self._api_call, method_name)

    def _api_call(self, method, *args):
        self.num_requests += 1
        data = json.dumps({
            'method': method,
            'params': args,
            'id': self.num_requests,
            'version': self.version
        })
        resp = requests.post(self.endpoint, data)
        if resp.status_code == 200:
            result = resp.json()
            return result
        else:
            raise requests.HTTPError(resp)
